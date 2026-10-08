# 📊 Vendas em E-commerce no Brasil — Projeto G1

**Disciplina:** Linguagem de Programação — Análise e Visualização de Dados com Python  
**Professor:** Alexandre Neves Louzada  
**Aluno:** Guilherme Oliveira de Moraes  

## 1. Sobre o projeto

Projeto acadêmico de análise e visualização de dados para investigar vendas em e-commerce no Brasil entre **2015 e 2024**. O pacote foi organizado para atender à estrutura exigida na avaliação: análise exploratória, tratamento dos dados, KPIs, gráficos, dashboard interativo, página HTML, persistência em SQLite e preparação para publicação.

> **Observação importante:** o PDF da avaliação disponibilizado para este trabalho não contém o CSV oficial. Por isso, este pacote usa uma **base simulada e reproduzível**, criada com 18.000 registros e com as colunas previstas no enunciado. Quando o professor fornecer o CSV oficial, ele pode substituir `dados/simulacao_ecommerce_brasil.csv` desde que mantenha a mesma estrutura de colunas.

## 2. Perguntas respondidas

- Quais categorias possuem maior faturamento?
- Quais estados concentram mais vendas?
- Existem períodos sazonais de maior consumo?
- Quais canais apresentam melhor desempenho?
- Quais produtos apresentam maior volume de vendas?
- Como o faturamento evoluiu ao longo do tempo?
- Existem regiões com maior ticket médio?
- Como o prazo de entrega se relaciona com a avaliação do cliente?

## 3. Tecnologias utilizadas

**Obrigatórias:** Python, Pandas, Matplotlib, Seaborn, Streamlit e GitHub.  
**Avançadas:** Plotly, SQLAlchemy, SQLite, NumPy e Jupyter Notebook.

## 4. Funcionalidades

### Dashboard
- filtros por ano, mês, região, estado, categoria e canal;
- KPIs dinâmicos;
- evolução temporal;
- faturamento por categoria;
- faturamento por estado;
- ranking de produtos;
- desempenho por canal;
- dispersão faturamento × lucro;
- heatmap de sazonalidade;
- análise de logística e avaliação;
- correlação estatística;
- interpretação textual dinâmica;
- conclusão executiva;
- tabela analítica;
- download da base completa em CSV;
- download do recorte filtrado em CSV.

### Funcionalidades avançadas
- persistência em **SQLite + SQLAlchemy**;
- gráficos interativos com **Plotly**.

## 5. Estrutura do projeto

```text
projeto-ecommerce/
├── app.py
├── requirements.txt
├── README.md
├── index.html
├── .gitignore
├── .streamlit/
│   └── config.toml
├── dados/
│   └── simulacao_ecommerce_brasil.csv
├── database/
│   ├── ecommerce.db
│   └── README.md
├── imagens/
│   ├── avaliacao_por_prazo.png
│   ├── evolucao_faturamento.png
│   ├── faturamento_categoria.png
│   ├── faturamento_canal.png
│   ├── faturamento_regiao.png
│   ├── heatmap_sazonalidade.png
│   └── scatter_lucro_faturamento.png
├── notebooks/
│   └── analise_ecommerce.ipynb
└── scripts/
    ├── gerar_base.py
    └── criar_banco.py
```


## 16. Identificação acadêmica

**Disciplina:** Linguagem de Programação — Análise e Visualização de Dados com Python  
**Professor:** Alexandre Neves Louzada  
**Aluno:** Guilherme Oliveira de Moraes
