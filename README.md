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

## 6. Como executar no Windows

### Criar ambiente virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Instalar dependências

```powershell
pip install -r requirements.txt
```

### Abrir o dashboard

```powershell
streamlit run app.py
```

### Abrir o notebook

```powershell
jupyter notebook notebooks/analise_ecommerce.ipynb
```

## 7. Recriar o banco SQLite

```powershell
python scripts/criar_banco.py
```

O banco será gravado em `database/ecommerce.db` na tabela `vendas`.

## 8. Conferir a base

```powershell
python -c "import pandas as pd; df=pd.read_csv('dados/simulacao_ecommerce_brasil.csv'); print(df.shape); print(df.head())"
```

## 9. Publicar no GitHub

```bash
git init
git add .
git commit -m "Projeto G1 - E-commerce Brasil"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/projeto-ecommerce.git
git push -u origin main
```

Troque `SEU-USUARIO` pelo seu usuário do GitHub.

## 10. Publicar no GitHub Pages

1. Entre no repositório no GitHub.
2. Abra **Settings → Pages**.
3. Em **Build and deployment**, selecione **Deploy from a branch**.
4. Escolha a branch `main`.
5. Escolha a pasta `/ (root)`.
6. Salve.
7. O `index.html` da raiz será usado como página do projeto.

## 11. Publicar no Streamlit Community Cloud

1. Faça o push do projeto para um repositório público.
2. Acesse o Streamlit Community Cloud.
3. Conecte sua conta do GitHub.
4. Crie uma nova aplicação.
5. Selecione o repositório.
6. Escolha `app.py` como arquivo principal.
7. Faça o deploy.

## 12. Links para preencher após a publicação

- **GitHub:** `https://github.com/SEU-USUARIO/projeto-ecommerce`
- **GitHub Pages:** `https://SEU-USUARIO.github.io/projeto-ecommerce/`
- **Streamlit:** `https://SEU-USUARIO-projeto-ecommerce.streamlit.app/`

O HTML possui botões e áreas preparadas para os links. Após publicar, ajuste os endereços no `index.html` para os seus links reais.

## 13. KPIs principais da base simulada

Na base incluída no pacote, sem filtros:

- **Faturamento total:** aproximadamente R$ 61,6 milhões;
- **Lucro total:** aproximadamente R$ 12,8 milhões;
- **Ticket médio por registro de venda:** aproximadamente R$ 3.420;
- **Categoria líder em faturamento:** Eletrônicos;
- **Região líder em faturamento:** Sudeste;
- **Estado líder em faturamento:** SP;
- **Canal líder em faturamento:** Site próprio;
- **Pico mensal:** novembro, seguido por dezembro;
- **Produto com maior volume:** Fone Bluetooth.

Esses valores são específicos da **base simulada deste pacote**.

## 14. Notebook

O notebook segue a sequência solicitada na avaliação:

1. introdução ao problema;
2. contextualização;
3. explicação da base;
4. leitura dos dados;
5. limpeza e preparação;
6. engenharia de atributos;
7. análise exploratória;
8. KPIs;
9. visualizações obrigatórias;
10. análise logística e correlação;
11. interpretação;
12. conclusão executiva.

## 15. Entrega acadêmica

O pacote foi organizado para facilitar as entregas exigidas:

- link do GitHub;
- link do GitHub Pages;
- link do Streamlit;
- notebook `.ipynb`;
- código `app.py`;
- base `.csv`;
- banco SQLite;
- página HTML;
- README com instruções.

## 16. Identificação acadêmica

**Disciplina:** Linguagem de Programação — Análise e Visualização de Dados com Python  
**Professor:** Alexandre Neves Louzada  
**Aluno:** Guilherme Oliveira de Moraes
