# Banco SQLite

A base SQLite foi recriada a partir de `dados/simulacao_ecommerce_brasil.csv`. O esquema relacional contém `fato_vendas`, dimensões de localidade, produto e canal, e a view integrada `vendas`. O campo `registro_id` é uma chave técnica criada no banco, não um ID de pedido existente no CSV. Recrie com `python scripts/criar_banco.py`.
