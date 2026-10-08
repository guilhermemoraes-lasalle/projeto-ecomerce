from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/"dados"/"simulacao_ecommerce_brasil.csv")
engine=create_engine(f"sqlite:///{(ROOT/'database'/'ecommerce.db').as_posix()}")
df.to_sql("vendas",engine,if_exists="replace",index=False,chunksize=1000)
for table,col in {"dim_regiao":"regiao","dim_uf":"uf","dim_cidade":"cidade","dim_canal":"canal_venda","dim_categoria":"categoria","dim_produto":"produto"}.items():
 df[[col]].drop_duplicates().rename(columns={col:"nome"}).to_sql(table,engine,if_exists="replace",index=False)
with engine.begin() as con:
 con.exec_driver_sql("CREATE INDEX IF NOT EXISTS idx_vendas_data ON vendas(data)")
 con.exec_driver_sql("CREATE INDEX IF NOT EXISTS idx_vendas_uf ON vendas(uf)")
print(f"Banco recriado: {len(df)} registros em vendas.")
