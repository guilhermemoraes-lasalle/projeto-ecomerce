from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

ROOT=Path(__file__).resolve().parents[1]
CSV=ROOT/"dados"/"simulacao_ecommerce_brasil.csv"
DB=ROOT/"database"/"ecommerce.db"
df=pd.read_csv(CSV)
engine=create_engine(f"sqlite:///{DB}")
df.to_sql("vendas",engine,if_exists="replace",index=False)
print(f"Banco criado: {DB}")
print(f"Registros: {len(df):,}".replace(",","."))
