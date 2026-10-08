from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "dados" / "simulacao_ecommerce_brasil.csv"
RNG = np.random.default_rng(42)
N = 18000

ufs = {
    "Sudeste": [("SP","São Paulo"),("RJ","Rio de Janeiro"),("MG","Belo Horizonte"),("ES","Vitória")],
    "Sul": [("PR","Curitiba"),("SC","Florianópolis"),("RS","Porto Alegre")],
    "Nordeste": [("BA","Salvador"),("CE","Fortaleza"),("PE","Recife"),("MA","São Luís"),("PB","João Pessoa")],
    "Centro-Oeste": [("GO","Goiânia"),("DF","Brasília"),("MT","Cuiabá"),("MS","Campo Grande")],
    "Norte": [("PA","Belém"),("AM","Manaus"),("RO","Porto Velho"),("TO","Palmas")],
}
region_probs = {"Sudeste":.43,"Nordeste":.20,"Sul":.18,"Centro-Oeste":.11,"Norte":.08}
regions = RNG.choice(list(region_probs), N, p=list(region_probs.values()))
uf_list, city_list = [], []
for region in regions:
    pairs = ufs[region]
    p = np.array([.40,.25,.18,.10,.07][:len(pairs)]); p /= p.sum()
    idx = RNG.choice(len(pairs), p=p)
    uf, city = pairs[idx]
    uf_list.append(uf); city_list.append(city)

years = RNG.choice(np.arange(2015,2025), N, p=np.array([.055,.06,.065,.075,.085,.095,.105,.11,.12,.23]))
month_probs = np.array([.07,.065,.07,.075,.08,.08,.08,.085,.10,.10,.14,.11]); month_probs /= month_probs.sum()
months = RNG.choice(np.arange(1,13), N, p=month_probs)
dates = pd.to_datetime({"year":years,"month":months,"day":1}) + pd.to_timedelta(RNG.integers(0,28,N), unit="D")

channels = ["Site próprio","Marketplace","Aplicativo","Social Commerce"]
canal = RNG.choice(channels, N, p=[.38,.34,.19,.09])

products = {
    "Eletrônicos": ["Smartphone Pro X","Fone Bluetooth","Smart TV 55","Notebook 15","Tablet 10"],
    "Casa": ["Jogo de Panelas","Aspirador Robô","Cafeteira","Liquidificador","Jogo de Cama"],
    "Esportes": ["Tênis Corrida","Bicicleta Urbana","Smartwatch Sport","Kit Academia","Mochila Esportiva"],
    "Moda": ["Tênis Casual","Jaqueta Jeans","Vestido Midi","Camiseta Premium","Calça Slim"],
    "Beleza": ["Kit Skincare","Perfume Floral","Secador Íon","Paleta Make","Massageador Facial"],
    "Mercado": ["Cesta de Mercearia","Café Especial","Azeite Premium","Kit Snacks","Suco Integral"],
    "Livros": ["Romance Best Seller","Livro de Negócios","Curso Preparatório","Livro Infantil","Coleção Ficção"],
}
cat_names = list(products)
cat_probs = np.array([.46,.16,.10,.095,.06,.055,.07]); cat_probs /= cat_probs.sum()
categoria = RNG.choice(cat_names, N, p=cat_probs)
produto = [RNG.choice(products[c]) for c in categoria]

base_price = {
"Smartphone Pro X":2499,"Fone Bluetooth":289,"Smart TV 55":3299,"Notebook 15":4299,"Tablet 10":1599,
"Jogo de Panelas":489,"Aspirador Robô":1299,"Cafeteira":399,"Liquidificador":279,"Jogo de Cama":249,
"Tênis Corrida":599,"Bicicleta Urbana":1499,"Smartwatch Sport":899,"Kit Academia":379,"Mochila Esportiva":299,
"Tênis Casual":349,"Jaqueta Jeans":299,"Vestido Midi":289,"Camiseta Premium":149,"Calça Slim":219,
"Kit Skincare":249,"Perfume Floral":329,"Secador Íon":379,"Paleta Make":159,"Massageador Facial":199,
"Cesta de Mercearia":119,"Café Especial":49,"Azeite Premium":42,"Kit Snacks":69,"Suco Integral":31,
"Romance Best Seller":59,"Livro de Negócios":89,"Curso Preparatório":249,"Livro Infantil":49,"Coleção Ficção":129}
price = np.array([base_price[p] for p in produto]) * RNG.uniform(.84,1.16,N)
quantity = np.clip(np.round(RNG.poisson(np.where(price>1000,1.35,2.1),N)+1),1,8).astype(int)
season = {1:.88,2:.86,3:.92,4:.95,5:1.00,6:1.03,7:1.04,8:1.10,9:1.14,10:1.18,11:1.42,12:1.30}
year_factor = {y:1+.055*(y-2015) for y in range(2015,2025)}
price *= np.array([season[m] for m in months]) ** .15 * np.array([year_factor[y] for y in years]) ** .15
faturamento = np.round(price*quantity,2)
base_margin = {"Eletrônicos":.245,"Casa":.275,"Esportes":.28,"Moda":.29,"Beleza":.32,"Mercado":.20,"Livros":.25}
channel_penalty = {"Site próprio":.02,"Marketplace":.07,"Aplicativo":.04,"Social Commerce":.05}
margin = np.array([base_margin[c] for c in categoria]) - np.array([channel_penalty[c] for c in canal]) + RNG.normal(0,.025,N)
margin = np.clip(margin,.08,.42)
custo = np.round(faturamento*(1-margin),2)
lucro = np.round(faturamento-custo,2)
region_days = {"Sudeste":3.4,"Sul":3.7,"Centro-Oeste":4.4,"Nordeste":4.8,"Norte":6.1}
prazo = np.array([region_days[r] for r in regions]) + np.array([.55 if c=="Marketplace" else 0 for c in canal]) + RNG.normal(0,1.05,N)
prazo = np.round(np.clip(prazo,1.2,11.5),1)
avaliacao = np.round(np.clip(4.75-.12*prazo+RNG.normal(0,.34,N),2.6,5.0),2)

df = pd.DataFrame({
"id_venda":[f"V{i:06d}" for i in range(1,N+1)], "ano":years, "mes":months, "data":dates.dt.date.astype(str),
"regiao":regions,"uf":uf_list,"cidade":city_list,"canal_venda":canal,"categoria":categoria,"produto":produto,
"quantidade":quantity,"preco_unitario":np.round(price,2),"faturamento":faturamento,"custo":custo,"lucro":lucro,
"prazo_entrega":prazo,"avaliacao_cliente":avaliacao}).sort_values(["data","id_venda"]).reset_index(drop=True)

CSV.parent.mkdir(exist_ok=True)
df.to_csv(CSV,index=False,encoding="utf-8-sig")
print(f"Base criada: {CSV}")
print(f"Linhas: {len(df):,}".replace(",","."))
print(f"Colunas: {len(df.columns)}")
