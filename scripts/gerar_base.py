"""A base oficial deste pacote é dados/simulacao_ecommerce_brasil.csv. Este script valida sua estrutura sem gerar dados artificiais."""
from pathlib import Path
import pandas as pd
p=Path(__file__).resolve().parents[1]/"dados"/"simulacao_ecommerce_brasil.csv"
df=pd.read_csv(p)
print(f"Base disponível: {len(df)} registros e {len(df.columns)} colunas; período {df.ano.min()}–{df.ano.max()}.")
