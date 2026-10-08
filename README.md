# Análise de Vendas em E-commerce no Brasil

**Aluno:** Guilherme Oliveira de Moraes  
**Disciplina:** Linguagem de Programação — Análise e Visualização de Dados com Python  
**Professor:** Alexandre Neves Louzada

## Projeto e pergunta de análise
Dashboard, notebook e banco de dados para explorar como faturamento e lucro variam no tempo e entre regiões, estados, categorias e canais, além de descrever prazo de entrega e avaliação. Os resultados são descritivos do CSV fornecido; a base não tem ID de venda nem dados de clientes.

## Base utilizada
`dados/simulacao_ecommerce_brasil.csv` é a base enviada pelo professor para este projeto. Contém **4,440 registros**, **16 colunas**, período de **2015-01 a 2024-12**, **5 regiões**, **20 UFs** e **37 cidades**. Não foram encontrados nulos nem duplicatas exatas. Valores monetários e demais indicadores não foram inventados; são agregações das colunas fornecidas.

## Principais resultados da base completa

- Faturamento agregado: **R$ 85.128.670,31**; lucro informado agregado: **R$ 26.886.927,79**; margem agregada: **31.6%**.
- Prazo médio informado: **8.51 dias**; avaliação média: **3.77/5**.
- Maiores contribuições por faturamento: região **Sudeste**, estado **RJ**, categoria **Beleza** e canal **Marketplace**.
- Mês com maior faturamento agregado: **11/2022**.

A coluna `lucro` foi preservada conforme fornecida. A soma de faturamento menos custo pode divergir do lucro informado; o notebook calcula essa diferença para transparência.

## Conteúdo e funcionalidades
- Dashboard Streamlit com filtros por ano, mês, região, UF, cidade, canal, categoria e produto; KPIs recalculados por recorte; upload CSV; tabelas, visualizações Plotly e download do recorte.
- Notebook com introdução, leitura, inspeção, limpeza, atributos derivados, EDA, KPIs, gráficos, interpretação e conclusão.
- SQLite com SQLAlchemy, tabela de vendas, dimensões de região, UF, cidade, canal, categoria e produto e índices analíticos.
- Gráficos PNG regenerados a partir da base real. `index.html` resume resultados para GitHub Pages.

## Executar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

Para recriar o banco a partir do CSV:

```bash
python scripts/criar_banco.py
```

Notebook: abra `notebooks/analise_ecommerce.ipynb` no Jupyter. Os caminhos funcionam com diretório atual na raiz do projeto ou dentro de `notebooks`.

## Tecnologias
Python, Pandas, NumPy, Matplotlib, Seaborn, Plotly, Streamlit, SQLite, SQLAlchemy e Jupyter.
