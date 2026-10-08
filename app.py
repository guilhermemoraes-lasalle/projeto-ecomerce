from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine

st.set_page_config(page_title="E-commerce Brasil | G1", page_icon="📊", layout="wide")

DISCIPLINA = "Linguagem de Programação — Análise e Visualização de Dados com Python"
PROFESSOR = "Alexandre Neves Louzada"
ALUNO = "Guilherme Oliveira de Moraes"
ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "dados" / "simulacao_ecommerce_brasil.csv"
DB_PATH = ROOT / "database" / "ecommerce.db"

st.markdown("""
<style>
.block-container {padding-top: 1.2rem; padding-bottom: 3rem;}
.hero {padding: 1.6rem; border-radius: 22px; background: linear-gradient(135deg,#0f172a,#1e293b 55%,#0369a1); color:white; margin-bottom:1rem;}
.hero h1{margin:0;font-size:2.3rem}.hero p{margin:.35rem 0;color:#dbeafe}.kpi{padding:1rem;border:1px solid #dbe3ee;border-radius:16px;background:white;min-height:112px;box-shadow:0 3px 12px rgba(15,23,42,.06)}.klabel{font-size:.82rem;color:#64748b}.kvalue{font-size:1.22rem;font-weight:800;margin-top:.25rem}.small{color:#64748b;font-size:.82rem}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        engine = create_engine(f"sqlite:///{DB_PATH}")
        df = pd.read_sql("SELECT * FROM vendas", engine)
    except Exception:
        df = pd.read_csv(CSV_PATH)
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    return df

def brl(v):
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

df=load_data()

st.markdown(f"""
<div class="hero">
<h1>📊 Vendas em E-commerce no Brasil</h1>
<p>Dashboard analítico para o período de 2015 a 2024.</p>
<p><b>Disciplina:</b> {DISCIPLINA}<br><b>Professor:</b> {PROFESSOR}<br><b>Aluno:</b> {ALUNO}</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("🔎 Filtros")
    if st.button("↺ Restaurar filtros", use_container_width=True):
        st.rerun()
    anos=sorted(df.ano.unique()); meses=sorted(df.mes.unique()); regioes=sorted(df.regiao.unique()); ufs=sorted(df.uf.unique()); categorias=sorted(df.categoria.unique()); canais=sorted(df.canal_venda.unique())
    sel_anos=st.multiselect("Ano",anos,default=anos)
    sel_meses=st.multiselect("Mês",meses,default=meses)
    sel_regioes=st.multiselect("Região",regioes,default=regioes)
    sel_ufs=st.multiselect("Estado (UF)",ufs,default=ufs)
    sel_categorias=st.multiselect("Categoria",categorias,default=categorias)
    sel_canais=st.multiselect("Canal",canais,default=canais)

f=df[df.ano.isin(sel_anos)&df.mes.isin(sel_meses)&df.regiao.isin(sel_regioes)&df.uf.isin(sel_ufs)&df.categoria.isin(sel_categorias)&df.canal_venda.isin(sel_canais)].copy()
if f.empty:
    st.error("Nenhum registro para o conjunto de filtros atual.")
    st.stop()

# KPIs
faturamento=f.faturamento.sum(); lucro=f.lucro.sum(); ticket=f.faturamento.mean();
produto_mais=f.groupby("produto").quantidade.sum().idxmax(); cat_top=f.groupby("categoria").lucro.sum().idxmax(); reg_top=f.groupby("regiao").faturamento.sum().idxmax()

st.subheader("Indicadores-chave")
cols=st.columns(6)
for col,(label,val) in zip(cols,[
    ("Faturamento total",brl(faturamento)),("Lucro total",brl(lucro)),("Ticket médio",brl(ticket)),
    ("Produto mais vendido",produto_mais),("Categoria mais lucrativa",cat_top),("Região com maior faturamento",reg_top)
]):
    col.markdown(f'<div class="kpi"><div class="klabel">{label}</div><div class="kvalue">{val}</div></div>',unsafe_allow_html=True)

st.caption(f"{len(f):,} registros no recorte atual | {f.quantidade.sum():,} unidades vendidas".replace(',','.'))
st.divider()

# Temporal
st.subheader("1. Evolução temporal")
tmp=f.groupby(f.data.dt.to_period("M"),as_index=False).faturamento.sum(); tmp["data"]=tmp["data"].dt.to_timestamp()
fig=px.line(tmp,x="data",y="faturamento",markers=True,labels={"data":"Data","faturamento":"Faturamento (R$)"},template="plotly_white")
fig.update_layout(margin=dict(l=10,r=10,t=10,b=10),hovermode="x unified")
st.plotly_chart(fig,use_container_width=True)

# Comparisons
c1,c2=st.columns(2)
with c1:
    st.subheader("2. Faturamento por categoria")
    cat=f.groupby("categoria",as_index=False).agg(faturamento=("faturamento","sum"),lucro=("lucro","sum")).sort_values("faturamento")
    fig=px.bar(cat,x="faturamento",y="categoria",orientation="h",text_auto='.2s',template="plotly_white")
    fig.update_layout(margin=dict(l=10,r=10,t=10,b=10)); st.plotly_chart(fig,use_container_width=True)
with c2:
    st.subheader("3. Faturamento por estado")
    uf=f.groupby("uf",as_index=False).faturamento.sum().sort_values("faturamento",ascending=False).head(15).sort_values("faturamento")
    fig=px.bar(uf,x="faturamento",y="uf",orientation="h",text_auto='.2s',template="plotly_white")
    fig.update_layout(margin=dict(l=10,r=10,t=10,b=10)); st.plotly_chart(fig,use_container_width=True)

# Products + channels
c1,c2=st.columns(2)
with c1:
    st.subheader("4. Top 10 produtos por volume")
    prod=f.groupby("produto",as_index=False).quantidade.sum().nlargest(10,"quantidade").sort_values("quantidade")
    fig=px.bar(prod,x="quantidade",y="produto",orientation="h",text_auto=True,template="plotly_white")
    st.plotly_chart(fig,use_container_width=True)
with c2:
    st.subheader("5. Desempenho por canal")
    ch=f.groupby("canal_venda",as_index=False).agg(faturamento=("faturamento","sum"),lucro=("lucro","sum"),vendas=("id_venda","count")).sort_values("faturamento",ascending=False)
    st.dataframe(ch.style.format({"faturamento":"R$ {:,.2f}","lucro":"R$ {:,.2f}","vendas":"{:,.0f}"}),use_container_width=True,hide_index=True)

# Required scatter
st.subheader("6. Relação entre faturamento e lucro")
amostra=f.sample(min(4000,len(f)),random_state=42)
fig=px.scatter(amostra,x="faturamento",y="lucro",color="categoria",hover_data=["produto","uf","canal_venda"],opacity=.65,template="plotly_white",labels={"faturamento":"Faturamento (R$)","lucro":"Lucro (R$)"})
fig.update_layout(margin=dict(l=10,r=10,t=10,b=10)); st.plotly_chart(fig,use_container_width=True)

# Required heatmap
st.subheader("7. Heatmap mensal de sazonalidade")
pivot=f.pivot_table(index="ano",columns="mes",values="faturamento",aggfunc="sum",fill_value=0)
fig,ax=plt.subplots(figsize=(12,4.7)); sns.heatmap(pivot,cmap="Blues",linewidths=.25,ax=ax); ax.set_xlabel("Mês"); ax.set_ylabel("Ano"); st.pyplot(fig,use_container_width=True); plt.close(fig)

# Logistics
st.subheader("8. Logística e satisfação")
faixa=pd.cut(f.prazo_entrega,bins=[0,3,5,7,20],labels=["Até 3 dias","4–5 dias","6–7 dias","Acima de 7 dias"])
log=f.assign(faixa_entrega=faixa).groupby("faixa_entrega",observed=False).agg(vendas=("id_venda","count"),faturamento=("faturamento","sum"),prazo_medio=("prazo_entrega","mean"),avaliacao_media=("avaliacao_cliente","mean")).reset_index()
st.dataframe(log.style.format({"faturamento":"R$ {:,.2f}","prazo_medio":"{:.1f}","avaliacao_media":"{:.2f}"}),use_container_width=True,hide_index=True)

corr=f[["faturamento","lucro","quantidade","prazo_entrega","avaliacao_cliente"]].corr(numeric_only=True)
fig,ax=plt.subplots(figsize=(7,4.8)); sns.heatmap(corr,annot=True,fmt=".2f",cmap="coolwarm",ax=ax); ax.set_title("Correlação entre indicadores"); st.pyplot(fig,use_container_width=True); plt.close(fig)

# Dynamic interpretation
mes_pico=int(f.groupby("mes").faturamento.sum().idxmax()); prazo=f.prazo_entrega.mean(); avaliacao=f.avaliacao_cliente.mean(); margem=lucro/faturamento
st.subheader("9. Interpretação textual")
st.info(f"No recorte atual, o faturamento é **{brl(faturamento)}**, o lucro é **{brl(lucro)}** e a margem líquida simulada é **{margem:.1%}**. A liderança está em **{reg_top}**, com a categoria **{cat_top}** como maior geradora de lucro. O produto com maior volume é **{produto_mais}**. O mês de maior faturamento acumulado é **{mes_pico}**. A logística apresenta prazo médio de **{prazo:.1f} dias**, enquanto a avaliação média é **{avaliacao:.2f}/5**.")

st.subheader("10. Conclusão executiva")
st.success("O recorte analisado mostra oportunidades principalmente em três frentes: concentrar planejamento comercial nos períodos de pico; acompanhar categorias e estados que sustentam a receita e o lucro; e reduzir prazos de entrega, já que a experiência do cliente apresenta relação mais relevante com a logística do que com o volume isolado de vendas.")

# Table / downloads
st.subheader("11. Tabela dinâmica")
tab=f.groupby(["ano","regiao","uf","categoria","canal_venda"],as_index=False).agg(vendas=("id_venda","count"),unidades=("quantidade","sum"),faturamento=("faturamento","sum"),custo=("custo","sum"),lucro=("lucro","sum"),prazo_medio=("prazo_entrega","mean"),avaliacao_media=("avaliacao_cliente","mean")).sort_values("faturamento",ascending=False)
st.dataframe(tab.style.format({"faturamento":"R$ {:,.2f}","custo":"R$ {:,.2f}","lucro":"R$ {:,.2f}","prazo_medio":"{:.1f}","avaliacao_media":"{:.2f}"}),use_container_width=True,hide_index=True)

st.subheader("12. Downloads")
d1,d2=st.columns(2)
with d1:
    st.download_button("⬇️ Baixar base completa (CSV)",data=df.to_csv(index=False).encode("utf-8-sig"),file_name="simulacao_ecommerce_brasil.csv",mime="text/csv",use_container_width=True)
with d2:
    st.download_button("⬇️ Baixar recorte filtrado (CSV)",data=f.to_csv(index=False).encode("utf-8-sig"),file_name="ecommerce_filtrado.csv",mime="text/csv",use_container_width=True)

with st.expander("ℹ️ Sobre a base e a avaliação"):
    st.write("A base deste pacote é simulada e reproduzível, com 18.000 registros de vendas no intervalo de 2015 a 2024. A estrutura foi construída para contemplar as colunas e perguntas orientadoras do enunciado acadêmico. Quando o CSV oficial do professor estiver disponível, ele pode substituir o arquivo em dados/ mantendo as mesmas colunas.")

st.divider(); st.caption(f"{DISCIPLINA} | Professor: {PROFESSOR} | Aluno: {ALUNO}")
