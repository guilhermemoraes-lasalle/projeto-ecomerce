"""Audita a base fornecida; não cria dados sintéticos."""
from pathlib import Path
import pandas as pd
p=Path(__file__).resolve().parents[1]/"dados"/"simulacao_ecommerce_brasil.csv"
df=pd.read_csv(p)
print("Dimensões:",df.shape,"| Nulos:",int(df.isna().sum().sum()),"| Duplicatas:",int(df.duplicated().sum()))
print("Período:",df.ano.min(),"a",df.ano.max())
