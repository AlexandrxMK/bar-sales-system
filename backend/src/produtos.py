class Produto:
    def __init__(self, id_produto, nome, marca, estoque, preco, validade, categoria, fabricado_em):
        self.id_produto = id_produto
        self.nome = nome
        self.marca = marca
        self.estoque = estoque
        self.preco = preco
        self.validade = validade
        self.categoria = categoria
        self.fabricado_em = fabricado_em


class Cliente:
    def __init__(self, id_cliente, nome, cidade, torce_flamengo, assiste_one_piece):
        self.id_cliente = id_cliente
        self.nome = nome
        self.cidade = cidade
        self.torce_flamengo = torce_flamengo
        self.assiste_one_piece = assiste_one_piece


class Vendedor:
    def __init__(self, id_vendedor, nome):
        self.id_vendedor = id_vendedor
        self.nome = nome


class Venda:
    def __init__(self, id_venda, id_cliente, id_vendedor, data_venda, valor_total):
        self.id_venda = id_venda
        self.id_cliente = id_cliente
        self.id_vendedor = id_vendedor
        self.data_venda = data_venda
        self.valor_total = valor_total


class ItemVenda:
    def __init__(self, id_venda, id_produto, quantidade, preco_unitario):
        self.id_venda = id_venda
        self.id_produto = id_produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario


class Pagamento:
    def __init__(self, id_pagamento, id_venda, metodo, status_confirmacao):
        self.id_pagamento = id_pagamento
        self.id_venda = id_venda
        self.metodo = metodo
        self.status_confirmacao = status_confirmacao
