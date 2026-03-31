from conexao import Conexao
import json
from produtos import Produto, Cliente, Vendedor, Venda, ItemVenda, Pagamento

db = Conexao()


# ========== PRODUTOS ==========

def cadastrar_produto(nome, marca, estoque, preco, validade, categoria, fabricado_em):
    """Insere um produto. Retorna ID ou lança exceção."""
    conexao, cursor = db.conectar()
    if not conexao:
        raise Exception("Erro ao conectar ao banco")

    try:
        sql = "INSERT INTO produtos (nome, marca, estoque, preco, validade, categoria, fabricado_em) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (nome, marca, estoque, preco,
                       validade, categoria, fabricado_em))
        conexao.commit()
        return cursor.lastrowid
    except Exception as e:
        conexao.rollback()
        raise
    finally:
        cursor.close()
        conexao.close()


def listar_todos():
    """Retorna lista de todos os produtos."""
    conexao, cursor = db.conectar()
    if not conexao:
        raise Exception("Erro ao conectar ao banco")

    try:
        cursor.execute("SELECT * FROM produtos")
        resultados = cursor.fetchall()
        return [Produto(*row) for row in resultados]
    except Exception as e:
        raise
    finally:
        cursor.close()
        conexao.close()


def obter_produto(id_produto):
    """Retorna um produto específico ou None."""
    conexao, cursor = db.conectar()
    if not conexao:
        raise Exception("Erro ao conectar ao banco")

    try:
        cursor.execute(
            "SELECT * FROM produtos WHERE id_produto = %s", (id_produto,))
        resultado = cursor.fetchone()
        return Produto(*resultado) if resultado else None
    except Exception as e:
        raise
    finally:
        cursor.close()
        conexao.close()


def pesquisar_por_nome(termo):
    """Retorna lista de produtos que contêm o termo no nome."""
    conexao, cursor = db.conectar()
    if not conexao:
        raise Exception("Erro ao conectar ao banco")

    try:
        cursor.execute(
            "SELECT * FROM produtos WHERE nome LIKE %s", (f"%{termo}%",))
        resultados = cursor.fetchall()
        return [Produto(*row) for row in resultados]
    except Exception as e:
        raise
    finally:
        cursor.close()
        conexao.close()


def alterar_preco(id_produto, novo_preco):
    """Atualiza o preço. Retorna True se atualizado, False se ID não existe."""
    conexao, cursor = db.conectar()
    if not conexao:
        raise Exception("Erro ao conectar ao banco")

    try:
        cursor.execute(
            "UPDATE produtos SET preco = %s WHERE id_produto = %s", (novo_preco, id_produto))
        conexao.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conexao.rollback()
        raise
    finally:
        cursor.close()
        conexao.close()


def remover_produto(id_produto):
    """Remove um produto. Retorna True se removido, False se não encontrado."""
    conexao, cursor = db.conectar()
    if not conexao:
        raise Exception("Erro ao conectar ao banco")

    try:
        cursor.execute(
            "DELETE FROM itens_venda WHERE id_produto = %s", (id_produto,))
        conexao.commit()
        cursor.execute(
            "DELETE FROM produtos WHERE id_produto = %s", (id_produto,))
        conexao.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conexao.rollback()
        raise
    finally:
        cursor.close()
        conexao.close()


def gerar_relatorio():
    """Retorna dicionário com estatísticas do estoque."""
    conexao, cursor = db.conectar()
    if not conexao:
        raise Exception("Erro ao conectar ao banco")

    try:
        cursor.execute("SELECT COUNT(*) FROM produtos")
        qtd_total = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(preco * estoque) FROM produtos")
        resultado = cursor.fetchone()[0]
        valor_total = resultado if resultado is not None else 0.0

        return {
            "quantidade_total": qtd_total,
            "valor_total": float(valor_total)
        }
    except Exception as e:
        raise
    finally:
        cursor.close()
        conexao.close()


def filtrar_por_preco(preco_min, preco_max):
    """Retorna produtos dentro da faixa de preço."""
    conexao, cursor = db.conectar()
    if not conexao:
        raise Exception("Erro ao conectar ao banco")

    try:
        cursor.execute(
            "SELECT * FROM produtos WHERE preco BETWEEN %s AND %s ORDER BY preco",
            (preco_min, preco_max)
        )
        resultados = cursor.fetchall()
        return [Produto(*row) for row in resultados]
    except Exception as e:
        raise
    finally:
        cursor.close()
        conexao.close()


def filtrar_por_categoria(categoria):
    """Retorna produtos da categoria especificada."""
    conexao, cursor = db.conectar()
    if not conexao:
        raise Exception("Erro ao conectar ao banco")

    try:
        cursor.execute(
            "SELECT * FROM produtos WHERE categoria LIKE %s",
            (f"%{categoria}%",)
        )
        resultados = cursor.fetchall()
        return [Produto(*row) for row in resultados]
    except Exception as e:
        raise
    finally:
        cursor.close()
        conexao.close()


def filtrar_por_cidade_fabricacao(cidade):
    """Retorna produtos fabricados na cidade especificada."""
    conexao, cursor = db.conectar()
    if not conexao:
        raise Exception("Erro ao conectar ao banco")

    try:
        cursor.execute(
            "SELECT * FROM produtos WHERE fabricado_em LIKE %s",
            (f"%{cidade}%",)
        )
        resultados = cursor.fetchall()
        return [Produto(*row) for row in resultados]
    except Exception as e:
        raise
    finally:
        cursor.close()
        conexao.close()


def listar_produtos_estoque_baixo():
    """Retorna produtos com estoque < 5."""
    conexao, cursor = db.conectar()
    if not conexao:
        raise Exception("Erro ao conectar ao banco")

    try:
        cursor.execute(
            "SELECT * FROM produtos WHERE estoque < 5 ORDER BY estoque")
        resultados = cursor.fetchall()
        return [Produto(*row) for row in resultados]
    except Exception as e:
        raise
    finally:
        cursor.close()
        conexao.close()


# ========== CLIENTES ==========

def cadastrar_cliente(nome, cidade, torce_flamengo, assiste_one_piece):
    """Insere um cliente. Retorna ID."""
    conexao, cursor = db.conectar()
    if not conexao:
        raise Exception("Erro ao conectar ao banco")

    try:
        sql = "INSERT INTO clientes (nome, cidade, torce_flamengo, assiste_one_piece) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (nome, cidade, int(
            torce_flamengo), int(assiste_one_piece)))
        conexao.commit()
        return cursor.lastrowid
    except Exception as e:
        conexao.rollback()
        raise
    finally:
        cursor.close()
        conexao.close()


def listar_clientes():
    """Retorna lista de clientes."""
    conexao, cursor = db.conectar()
    if not conexao:
        raise Exception("Erro ao conectar ao banco")

    try:
        cursor.execute("SELECT * FROM clientes")
        resultados = cursor.fetchall()
        return [Cliente(*row) for row in resultados]
    except Exception as e:
        raise
    finally:
        cursor.close()
        conexao.close()


def obter_cliente(id_cliente):
    """Retorna um cliente específico."""
    conexao, cursor = db.conectar()
    if not conexao:
        raise Exception("Erro ao conectar ao banco")

    try:
        cursor.execute(
            "SELECT * FROM clientes WHERE id_cliente = %s", (id_cliente,))
        resultado = cursor.fetchone()
        return Cliente(*resultado) if resultado else None
    except Exception as e:
        raise
    finally:
        cursor.close()
        conexao.close()


# ========== VENDEDORES ==========

def cadastrar_vendedor(nome):
    """Insere um vendedor. Retorna ID."""
    conexao, cursor = db.conectar()
    if not conexao:
        raise Exception("Erro ao conectar ao banco")

    try:
        cursor.execute("INSERT INTO vendedores (nome) VALUES (%s)", (nome,))
        conexao.commit()
        return cursor.lastrowid
    except Exception as e:
        conexao.rollback()
        raise
    finally:
        cursor.close()
        conexao.close()


def listar_vendedores():
    """Retorna lista de vendedores."""
    conexao, cursor = db.conectar()
    if not conexao:
        raise Exception("Erro ao conectar ao banco")

    try:
        cursor.execute("SELECT * FROM vendedores")
        resultados = cursor.fetchall()
        return [Vendedor(*row) for row in resultados]
    except Exception as e:
        raise
    finally:
        cursor.close()
        conexao.close()


def obter_vendedor(id_vendedor):
    """Retorna um vendedor específico."""
    conexao, cursor = db.conectar()
    if not conexao:
        raise Exception("Erro ao conectar ao banco")

    try:
        cursor.execute(
            "SELECT * FROM vendedores WHERE id_vendedor = %s", (id_vendedor,))
        resultado = cursor.fetchone()
        return Vendedor(*resultado) if resultado else None
    except Exception as e:
        raise
    finally:
        cursor.close()
        conexao.close()


# ========== VENDAS ==========

def calcular_desconto(id_cliente):
    """Calcula desconto baseado nas preferências do cliente."""
    conexao, cursor = db.conectar()
    if not conexao:
        raise Exception("Erro ao conectar ao banco")

    try:
        cursor.execute(
            "SELECT cidade, torce_flamengo, assiste_one_piece FROM clientes WHERE id_cliente = %s",
            (id_cliente,)
        )
        cliente = cursor.fetchone()

        if not cliente:
            return 0

        cidade, flamengo, one_piece = cliente
        desconto = 0

        if flamengo == 1:
            desconto += 10
        if one_piece == 1:
            desconto += 10
        if cidade and cidade.lower() == 'sousa':
            desconto += 10

        return min(desconto, 30)
    except Exception as e:
        raise
    finally:
        cursor.close()
        conexao.close()


def registrar_venda(id_cliente, id_vendedor, itens, metodo_pagamento):
    """
    Registra uma venda completa.

    Args:
        id_cliente: int
        id_vendedor: int
        itens: lista de tuplas [(id_produto, quantidade), ...]
        metodo_pagamento: str

    Returns:
        dict com dados da venda criada
    """
    conexao, cursor = db.conectar()
    if not conexao:
        raise Exception("Erro ao conectar ao banco")

    try:
        # Prepara a lista de itens no formato JSON esperado pela stored procedure.
        itens_json_list = []
        for id_prod, qtd in itens:
            itens_json_list.append({"id_produto": id_prod, "quantidade": qtd})
        p_itens_json = json.dumps(itens_json_list)

        # Chama a stored procedure 'finalizar_venda'
        cursor.callproc('finalizar_venda', (id_cliente,
                        id_vendedor, p_itens_json, metodo_pagamento))
        conexao.commit()
        return True
    except Exception as e:
        conexao.rollback()
        raise
    finally:
        cursor.close()
        conexao.close()


def listar_vendas():
    """Retorna lista de todas as vendas."""
    conexao, cursor = db.conectar()
    if not conexao:
        raise Exception("Erro ao conectar ao banco")

    try:
        cursor.execute("""
            SELECT v.id_venda, c.nome, ve.nome, v.data_venda, v.valor_total
            FROM vendas v
            JOIN clientes c ON v.id_cliente = c.id_cliente
            JOIN vendedores ve ON v.id_vendedor = ve.id_vendedor
            ORDER BY v.data_venda DESC
        """)
        return cursor.fetchall()
    except Exception as e:
        raise
    finally:
        cursor.close()
        conexao.close()


def obter_historico_cliente(id_cliente):
    """Retorna histórico de vendas de um cliente com itemização."""
    conexao, cursor = db.conectar()
    if not conexao:
        raise Exception("Erro ao conectar ao banco")

    try:
        # Dados do cliente
        cursor.execute(
            "SELECT * FROM clientes WHERE id_cliente = %s", (id_cliente,))
        cliente_data = cursor.fetchone()
        if not cliente_data:
            raise ValueError(f"Cliente {id_cliente} não encontrado")

        cliente = Cliente(*cliente_data)

        # Vendas do cliente
        cursor.execute("""
            SELECT v.id_venda, v.data_venda, v.valor_total, ve.nome
            FROM vendas v
            JOIN vendedores ve ON v.id_vendedor = ve.id_vendedor
            WHERE v.id_cliente = %s
            ORDER BY v.data_venda DESC
        """, (id_cliente,))

        vendas = cursor.fetchall()
        vendas_detalhadas = []

        for id_venda, data, total, vendedor in vendas:
            # Itens da venda
            cursor.execute("""
                SELECT p.nome, iv.quantidade, iv.preco_unitario
                FROM itens_venda iv
                JOIN produtos p ON iv.id_produto = p.id_produto
                WHERE iv.id_venda = %s
            """, (id_venda,))

            itens = cursor.fetchall()
            vendas_detalhadas.append({
                "id_venda": id_venda,
                "data": data,
                "total": total,
                "vendedor": vendedor,
                "itens": itens
            })

        return {
            "cliente": cliente,
            "desconto_atual": calcular_desconto(id_cliente),
            "vendas": vendas_detalhadas
        }
    except Exception as e:
        raise
    finally:
        cursor.close()
        conexao.close()


def gerar_relatorio_vendas():
    """Retorna relatório mensal de vendas por vendedor."""
    conexao, cursor = db.conectar()
    if not conexao:
        raise Exception("Erro ao conectar ao banco")

    try:
        cursor.execute("SELECT * FROM relatorio_vendas_mensal")
        return cursor.fetchall()
    except Exception as e:
        raise
    finally:
        cursor.close()
        conexao.close()
