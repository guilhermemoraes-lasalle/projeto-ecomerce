# Vendas em E-commerce no Brasil — Projeto G1

**Disciplina:** Linguagens de Programação  
**Professor:** Alexandre Neves Louzada  
**Aluno:** Guilherme Oliveira de Moraes

## Publicações

- GitHub: https://github.com/guilhermemoraes-lasalle/projeto-ecomerce
- GitHub Pages: https://guilhermemoraes-lasalle.github.io/projeto-ecomerce/
- Streamlit: https://projeto-ecomerce-atrtcjstuvrclmvl2gvbng.streamlit.app/

## Objetivo e base
Analisar o comportamento de vendas em e-commerce no Brasil, comparando períodos, categorias, produtos, canais, regiões, UFs e indicadores logísticos. A base indicada para este projeto tem **4,440 registros e 16 colunas**, cobrindo **2015-01 a 2024-12**. Não há valores nulos ou duplicatas exatas.

### Indicadores calculados da base

- Faturamento total: **R$ 85.128.670,31**
- Lucro total informado no CSV: **R$ 26.886.927,79**
- Faturamento médio por registro: **R$ 19.173,12**
- Região/UF de maior faturamento: **Sudeste / RJ**
- Canal de maior faturamento: **Marketplace**
- Categoria com maior soma de lucro informado: **Beleza**
- Produto com mais unidades: **Produto D**
- Mês de pico acumulado: **11/2022**
- Prazo médio: **8.51 dias**; avaliação média: **3.77/5**

**Limites:** a fonte não tem identificador de pedido, portanto a média é por registro e não ticket médio por pedido. A coluna `lucro` foi mantida como recebida; pode divergir de `faturamento - custo` (maior diferença absoluta observada: R$ 16.719,74). Correlações são descritivas, não causais.

## Dashboard e critérios atendidos

O app contém título e problema de análise, filtros por ano, mês, região, UF, categoria, canal, cidade e produto; KPIs dinâmicos; upload; seções; tabelas; linha temporal; comparações por categoria, estado e região; ranking de produtos; dispersão lucro × faturamento; heatmap; logística, satisfação, correlação e conclusão executiva. Usa Python, Pandas, Matplotlib, Seaborn, Streamlit, Plotly, SQLAlchemy e SQLite.

O banco relacional tem fato de vendas e dimensões de localidade, produto e canal. `registro_id` é uma chave técnica criada no banco e não representa ID de pedido na fonte.

## Estrutura

```text
projeto-ecommerce/
├── app.py
├── requirements.txt
├── README.md
├── index.html
├── .streamlit/config.toml
├── dados/simulacao_ecommerce_brasil.csv
├── database/ecommerce.db
├── imagens/*.png
├── notebooks/analise_ecommerce.ipynb
└── scripts/
```

## Como executar no Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Para recriar o SQLite: `python scripts/criar_banco.py`. Abra `notebooks/analise_ecommerce.ipynb` no Jupyter para reproduzir a análise e os gráficos. O HTML na raiz é a página do GitHub Pages; os links de publicação acima já estão preenchidos.
