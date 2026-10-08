from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine

st.set_page_config(page_title="E-commerce Brasil",page_icon="📊",layout="wide")
ROOT=Path(__file__).resolve().parent; CSV=ROOT/'dados'/'simulacao_ecommerce_brasil.csv'; DB=ROOT/'database'/'ecommerce.db'
ALUNO='Guilherme Oliveira de Moraes'; DISCIPLINA='Linguagem de Programação — Análise e Visualização de Dados com Python'; PROFESSOR='Alexandre Neves Louzada'
@st.cache_data
def carregar():
    try:
        x=pd.read_sql('SELECT * FROM vendas',create_engine(f"sqlite:///{DB.as_posix()}"))
    except Exception: x=pd.read_csv(CSV)
    x['data']=pd.to_datetime(x['data'],errors='coerce'); return x
base=carregar()
st.title('📊 Análise de Vendas em E-commerce no Brasil')
st.caption(f'{DISCIPLINA} · Professor: {PROFESSOR} · Aluno: {ALUNO}')
st.markdown('**Problema:** compreender a evolução das vendas, a contribuição de produtos, canais e localidades e a relação entre logística e satisfação, para apoiar decisões comerciais baseadas nesta base acadêmica.')
with st.sidebar:
    st.header('Filtros')
    upload=st.file_uploader('Carregar outro CSV com as mesmas colunas',type=['csv'])
    if upload:
        try: base=pd.read_csv(upload); base['data']=pd.to_datetime(base['data'],errors='coerce'); st.success('Arquivo carregado para esta sessão.')
        except Exception as e: st.error(f'Não foi possível ler o CSV: {e}')
    yrs=sorted(base.ano.dropna().unique().tolist()); months=sorted(base.mes.dropna().unique().tolist())
    years=st.multiselect('Ano',yrs,yrs); msel=st.multiselect('Mês',months,months)
    for col,label in [('regiao','Região'),('uf','UF'),('cidade','Cidade'),('canal_venda','Canal'),('categoria','Categoria'),('produto','Produto')]:
        opts=sorted(base[col].dropna().unique().tolist()); locals()[col+'_sel']=st.multiselect(label,opts,opts)
    regs=locals()['regiao_sel']; ufs=locals()['uf_sel']; cities=locals()['cidade_sel']; chans=locals()['canal_venda_sel']; cats=locals()['categoria_sel']; prods=locals()['produto_sel']
f=base[base.ano.isin(years)&base.mes.isin(msel)&base.regiao.isin(regs)&base.uf.isin(ufs)&base.cidade.isin(cities)&base.canal_venda.isin(chans)&base.categoria.isin(cats)&base.produto.isin(prods)].copy()
if f.empty: st.warning('Nenhuma venda corresponde aos filtros.'); st.stop()
revenue=f.faturamento.sum(); profit=f.lucro.sum(); margin=profit/revenue if revenue else 0
k=st.columns(5)
for c,(label,value) in zip(k,[('Faturamento',f'R$ {revenue:,.2f}'),('Lucro informado',f'R$ {profit:,.2f}'),('Margem informada',f'{margin:.1%}'),('Vendas (linhas)',f'{len(f):,}'),('Unidades',f'{f.quantidade.sum():,}')]): c.metric(label,value)
st.caption(f"Recorte de {f.data.min():%d/%m/%Y} a {f.data.max():%d/%m/%Y} · ticket médio por registro {('R$ {:,.2f}'.format(f.faturamento.mean()))}")
st.subheader('Evolução temporal')
t=f.groupby(f.data.dt.to_period('M')).faturamento.sum().rename_axis('mês').reset_index(); t['mês']=t['mês'].dt.to_timestamp()
st.plotly_chart(px.line(t,x='mês',y='faturamento',markers=True,title='Faturamento por mês',template='plotly_white'),use_container_width=True)
a,b=st.columns(2)
with a: st.plotly_chart(px.bar(f.groupby('categoria',as_index=False).faturamento.sum().sort_values('faturamento'),x='faturamento',y='categoria',orientation='h',title='Faturamento por categoria',template='plotly_white'),use_container_width=True)
with b: st.plotly_chart(px.bar(f.groupby('uf',as_index=False).faturamento.sum().nlargest(15,'faturamento'),x='uf',y='faturamento',title='Estados por faturamento',template='plotly_white'),use_container_width=True)
a,b=st.columns(2)
with a: st.plotly_chart(px.bar(f.groupby('canal_venda',as_index=False).faturamento.sum(),x='canal_venda',y='faturamento',color='canal_venda',title='Comparação entre canais'),use_container_width=True)
with b: st.plotly_chart(px.scatter(f,x='faturamento',y='lucro',color='categoria',hover_data=['uf','produto','canal_venda'],title='Faturamento e lucro'),use_container_width=True)
st.subheader('Sazonalidade e logística')
a,b=st.columns(2)
with a:
 p=f.pivot_table(index='ano',columns='mes',values='faturamento',aggfunc='sum'); fig,ax=plt.subplots(figsize=(10,4)); sns.heatmap(p,cmap='Blues',ax=ax); ax.set_title('Faturamento por ano e mês'); st.pyplot(fig); plt.close(fig)
with b:
 log=f.assign(faixa=pd.cut(f.prazo_entrega,[0,3,5,7,20],labels=['Até 3','4–5','6–7','Acima de 7'])).groupby('faixa',observed=False).agg(registros=('prazo_entrega','size'),prazo_medio=('prazo_entrega','mean'),avaliacao_media=('avaliacao_cliente','mean')).reset_index(); st.dataframe(log,use_container_width=True,hide_index=True)
st.subheader('Resumo por localidade, categoria e canal')
tab=f.groupby(['regiao','uf','cidade','categoria','canal_venda'],as_index=False).agg(registros=('data','size'),unidades=('quantidade','sum'),faturamento=('faturamento','sum'),custo=('custo','sum'),lucro=('lucro','sum'),prazo_medio=('prazo_entrega','mean'),avaliacao_media=('avaliacao_cliente','mean')).sort_values('faturamento',ascending=False)
st.dataframe(tab,use_container_width=True,hide_index=True)
st.subheader('Interpretação e conclusão executiva')
reg=f.groupby('regiao').faturamento.sum().idxmax(); cat=f.groupby('categoria').lucro.sum().idxmax(); can=f.groupby('canal_venda').faturamento.sum().idxmax(); pico=f.groupby(f.data.dt.to_period('M')).faturamento.sum().idxmax(); corr=f[['prazo_entrega','avaliacao_cliente']].corr().iloc[0,1]
st.info(f"Neste recorte, {reg} lidera o faturamento por região; {cat} gera o maior lucro agregado; e {can} tem maior faturamento entre os canais. O mês de pico é {pico:%m/%Y}. A correlação linear entre prazo de entrega e avaliação é {corr:.2f}; correlação isolada não demonstra causalidade.")
st.write('Priorize decisões com base nos segmentos que lideram o recorte, acompanhe a evolução mês a mês e investigue operacionalmente a associação entre entrega e satisfação antes de atribuir causa. Os resultados mudam com os filtros.')
st.download_button('Baixar recorte filtrado em CSV',f.to_csv(index=False).encode('utf-8-sig'),'ecommerce_filtrado.csv','text/csv')
with st.expander('Sobre a base e seus limites'):
 st.write(f"Base fornecida para o trabalho, com {len(base):,} registros e {base.data.min():%Y}–{base.data.max():%Y}. Cada linha é tratada como um registro de venda; o arquivo não possui identificador de venda nem tabelas de clientes. Os valores apresentados são estatísticas descritivas dos dados fornecidos.")
