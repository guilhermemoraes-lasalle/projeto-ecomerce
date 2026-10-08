from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text, event
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/"dados"/"simulacao_ecommerce_brasil.csv")
engine=create_engine(f"sqlite:///{(ROOT/'database'/'ecommerce.db').as_posix()}")
@event.listens_for(engine,"connect")
def enable_foreign_keys(dbapi_connection, record): dbapi_connection.execute("PRAGMA foreign_keys=ON")
with engine.begin() as con:
    con.exec_driver_sql("DROP VIEW IF EXISTS vendas")
    for t in ("fato_vendas","dim_localidade","dim_produto","dim_canal"): con.exec_driver_sql(f"DROP TABLE IF EXISTS {t}")
    con.exec_driver_sql("CREATE TABLE dim_localidade(id INTEGER PRIMARY KEY,regiao TEXT NOT NULL,uf TEXT NOT NULL,cidade TEXT NOT NULL,UNIQUE(regiao,uf,cidade))")
    con.exec_driver_sql("CREATE TABLE dim_produto(id INTEGER PRIMARY KEY,categoria TEXT NOT NULL,produto TEXT NOT NULL,UNIQUE(categoria,produto))")
    con.exec_driver_sql("CREATE TABLE dim_canal(id INTEGER PRIMARY KEY,canal_venda TEXT NOT NULL UNIQUE)")
    con.exec_driver_sql("CREATE TABLE fato_vendas(registro_id INTEGER PRIMARY KEY,ano INT,mes INT,data TEXT,localidade_id INT REFERENCES dim_localidade(id),produto_id INT REFERENCES dim_produto(id),canal_id INT REFERENCES dim_canal(id),quantidade INT,preco_unitario REAL,faturamento REAL,custo REAL,lucro REAL,prazo_entrega REAL,avaliacao_cliente REAL)")
    for t,fields in [("dim_localidade",["regiao","uf","cidade"]),("dim_produto",["categoria","produto"]),("dim_canal",["canal_venda"])]:
        con.execute(text("INSERT INTO "+t+"("+",".join(fields)+") VALUES("+",".join(":"+x for x in fields)+")"),df[fields].drop_duplicates().to_dict("records"))
    loc={(r.regiao,r.uf,r.cidade):r.id for r in con.execute(text("SELECT id,regiao,uf,cidade FROM dim_localidade"))}
    prod={(r.categoria,r.produto):r.id for r in con.execute(text("SELECT id,categoria,produto FROM dim_produto"))}
    canal={r.canal_venda:r.id for r in con.execute(text("SELECT id,canal_venda FROM dim_canal"))}
    rows=[]
    for i,r in enumerate(df.itertuples(index=False),1): rows.append(dict(registro_id=i,ano=int(r.ano),mes=int(r.mes),data=str(r.data),localidade_id=loc[(r.regiao,r.uf,r.cidade)],produto_id=prod[(r.categoria,r.produto)],canal_id=canal[r.canal_venda],quantidade=int(r.quantidade),preco_unitario=float(r.preco_unitario),faturamento=float(r.faturamento),custo=float(r.custo),lucro=float(r.lucro),prazo_entrega=float(r.prazo_entrega),avaliacao_cliente=float(r.avaliacao_cliente)))
    con.execute(text("INSERT INTO fato_vendas VALUES(:registro_id,:ano,:mes,:data,:localidade_id,:produto_id,:canal_id,:quantidade,:preco_unitario,:faturamento,:custo,:lucro,:prazo_entrega,:avaliacao_cliente)"),rows)
    con.exec_driver_sql("CREATE INDEX idx_fato_data ON fato_vendas(data)")
    con.exec_driver_sql("CREATE INDEX idx_fato_localidade ON fato_vendas(localidade_id)")
    con.exec_driver_sql("CREATE INDEX idx_fato_produto ON fato_vendas(produto_id)")
    con.exec_driver_sql("CREATE VIEW vendas AS SELECT f.registro_id,f.ano,f.mes,f.data,l.regiao,l.uf,l.cidade,c.canal_venda,p.categoria,p.produto,f.quantidade,f.preco_unitario,f.faturamento,f.custo,f.lucro,f.prazo_entrega,f.avaliacao_cliente FROM fato_vendas f JOIN dim_localidade l ON f.localidade_id=l.id JOIN dim_produto p ON f.produto_id=p.id JOIN dim_canal c ON f.canal_id=c.id")
print(f"Banco SQLite relacional recriado: {len(df)} registros.")
