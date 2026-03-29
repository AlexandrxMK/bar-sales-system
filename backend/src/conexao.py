import mysql.connector

class Conexao:

    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.database = 'BAR'

    def conectar(self):
        try:
            conexao = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            cursor = conexao.cursor()

            return conexao, cursor

        except Exception as erro:
            print(f"Erro de conexão: {erro}")
            return None, None