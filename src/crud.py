from conexao import Conexao
from produtos import Produto

db = Conexao()  # Cria uma instância da classe Conexao


def cadastrar_produto():
    print("\n--- CADASTRAR PRODUTO ---")
    nome = input("Nome da Bebida: ")
    marca = input("Marca: ")
    estoque = int(input("Quantidade em Estoque: "))
    preco = float(input("Preço (R$): "))
    validade = input("Validade (AAAA-MM-DD): ")

    conexao, cursor = db.conectar()
    if conexao:
        try:
            sql = "INSERT INTO produtos (nome, marca, estoque, preco, validade) VALUES (%s, %s, %s, %s, %s)"
            valores = (nome, marca, estoque, preco, validade)
            cursor.execute(sql, valores)
            conexao.commit()
            print(">>> Produto cadastrado com sucesso!")
        except Exception as e:
            print(f"Erro ao cadastrar: {e}")
        finally:
            cursor.close()
            conexao.close()


def listar_todos():
    print("\n--- LISTA DE ESTOQUE ---")
    conexao, cursor = db.conectar()
    if conexao:
        try:
            cursor.execute("SELECT * FROM produtos")
            resultados = cursor.fetchall()

            if not resultados:
                print("Nenhum produto cadastrado.")
            else:
                print(
                    f"{'ID':<5} | {'NOME':<20} | {'MARCA':<15} | {'QTD':<5} | {'PREÇO':<10} | {'VALIDADE'}")
                print("-" * 85)

                for item in resultados:
                    produto = Produto(*item)
                    print(
                        f"{produto.id_bebida:<5} | {produto.nome:<20} | {produto.marca:<15} | {produto.estoque:<5} | R$ {produto.preco:<8.2f} | {produto.validade}")

        except Exception as e:
            print(f"Erro ao ler dados: {e}")
        finally:
            cursor.close()
            conexao.close()


def pesquisar_por_nome():

    print("\n--- PESQUISAR PRODUTO ---")
    termo = input("Digite o nome (ou parte dele) para buscar: ")

    conexao, cursor = db.conectar()
    if conexao:
        # O %s com os % em volta serve para buscar qualquer parte do texto
        sql = "SELECT * FROM produtos WHERE nome LIKE %s"
        cursor.execute(sql, (f"%{termo}%",))
        resultados = cursor.fetchall()

        if not resultados:
            print("Nenhum produto encontrado com esse nome.")
        else:
            for item in resultados:
                produto = Produto(*item)
                print(
                    f"ACHEI: ID {produto.id_bebida} - {produto.nome} ({produto.marca}) - R$ {produto.preco}")
        cursor.close()
        conexao.close()


def alterar_preco():

    print("\n--- ALTERAR PREÇO ---")
    id_prod = input("Digite o ID do produto que quer alterar: ")
    novo_preco = float(input("Digite o NOVO preço: "))

    conexao, cursor = db.conectar()
    if conexao:
        sql = "UPDATE produtos SET preco = %s WHERE id_bebida = %s"
        cursor.execute(sql, (novo_preco, id_prod))
        conexao.commit()

        if cursor.rowcount > 0:
            print(">>> Preço atualizado!")
        else:
            print(">>> Erro: ID não encontrado.")

        cursor.close()
        conexao.close()


def remover_produto():
    print("\n--- REMOVER PRODUTO ---")
    id_prod = input("Digite o ID do produto para remover: ")

    conexao, cursor = db.conectar()
    if conexao:
        sql = "DELETE FROM vendas WHERE id_produto = %s"
        cursor.execute(sql, (id_prod,))
        conexao.commit()
        sql = "DELETE FROM produtos WHERE id_bebida = %s"
        cursor.execute(sql, (id_prod,))
        conexao.commit()

        if cursor.rowcount > 0:
            print(">>> Produto removido do estoque!")
        else:
            print(">>> Erro: ID não encontrado.")

        cursor.close()
        conexao.close()


def exibir_um():
    print("\n--- EXIBIR UM PRODUTO ---")
    id_busca = input("Digite o ID do produto: ")

    conexao, cursor = db.conectar()
    if conexao:
        cursor.execute(
            "SELECT * FROM produtos WHERE id_bebida = %s", (id_busca,))
        item = cursor.fetchone()

        if item:

            produto = Produto(*item)

            print("-" * 30)
            print(f"ID: {produto.id_bebida}")
            print(f"Nome: {produto.nome}")
            print(f"Marca: {produto.marca}")
            print(f"Estoque: {produto.estoque}")
            print(f"Preço: R$ {produto.preco}")
            print(f"Validade: {produto.validade}")

        else:
            print("Produto não encontrado.")

        cursor.close()
        conexao.close()


def gerar_relatorio():
    print("\n--- RELATÓRIO DO BAR ---")
    conexao, cursor = db.conectar()
    if conexao:

        cursor.execute("SELECT COUNT(*) FROM produtos")
        qtd_total = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(preco * estoque) FROM produtos")
        resultado_valor = cursor.fetchone()[0]
        valor_total = resultado_valor if resultado_valor is not None else 0.0

        print(f"Total de Itens Cadastrados: {qtd_total}")
        print(f"Valor Total em Estoque: R$ {valor_total:.2f}")

        cursor.close()
        conexao.close()


def registrar_venda():
    print("\n--- REGISTRAR VENDA ---")
    listar_todos()

    id_prod = input("\nDigite o ID do produto vendido: ")
    qtd_vendida = int(input("Quantidade vendida: "))

    conexao, cursor = db.conectar()
    if conexao:
        try:
            cursor.execute(
                "SELECT preco, estoque FROM produtos WHERE id_bebida = %s", (id_prod,))
            resultado = cursor.fetchone()

            if not resultado:
                print("Produto não encontrado!")
                return

            preco_atual = resultado[0]
            estoque_atual = resultado[1]

            if estoque_atual < qtd_vendida:
                print(f"Erro: Estoque insuficiente! Só tem {estoque_atual}.")
                return

            valor_final = preco_atual * qtd_vendida

            sql_venda = "INSERT INTO vendas (id_produto, quantidade, valor_total) VALUES (%s, %s, %s)"
            cursor.execute(sql_venda, (id_prod, qtd_vendida, valor_final))

            sql_estoque = "UPDATE produtos SET estoque = estoque - %s WHERE id_bebida = %s"
            cursor.execute(sql_estoque, (qtd_vendida, id_prod))

            conexao.commit()
            print(f">>> Venda registrada! Total: R$ {valor_final:.2f}")
            print(">>> Estoque atualizado.")

        except Exception as e:
            print(f"Erro ao registrar venda: {e}")
            conexao.rollback()  # Desfaz se der erro no meio
        finally:
            cursor.close()
            conexao.close()
