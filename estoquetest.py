import sqlite3

class Gestao:
    def __init__(self, banco):
        self.conn = sqlite3.connect(banco)
        self.criar_tabela_estoque()
    
    def criar_tabela_estoque(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estoque (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                codigo TEXT NOT NULL UNIQUE,
                quantidade INTEGER NOT NULL,
                quantidade_minima INTEGER NOT NULL,
                categoria TEXT
            )
        ''')
        self.conn.commit()

    def adicionar_produto(self, nome, codigo, quantidade, quantidade_minima, categoria):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO estoque (nome, codigo, quantidade, quantidade_minima, categoria)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, codigo, quantidade, quantidade_minima, categoria))
        self.conn.commit()

    def remover_produto(self, codigo, quantidade):
        cursor = self.conn.cursor()
        cursor.execute("SELECT quantidade FROM estoque WHERE codigo=?", (codigo,))
        resultado = cursor.fetchone()
        if resultado:
            estoque_atual = resultado[0]
            if estoque_atual >= quantidade:
                novo_estoque = estoque_atual - quantidade
                cursor.execute("UPDATE estoque SET quantidade=? WHERE codigo=?", (novo_estoque, codigo))
                self.conn.commit()
                self.verificar_reposicao(codigo)  # Verificação de reposição caso esteja abaixo do mínimo blabla
            else:
                print(f"Quantidade insuficiente de {codigo} em estoque.")
        else:
            print(f"Produto com código {codigo} não encontrado em estoque.")

    def consultar_estoque(self, codigo):
        cursor = self.conn.cursor()
        cursor.execute("SELECT quantidade FROM estoque WHERE codigo=?", (codigo,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        else:
            return 0

    def verificar_reposicao(self, codigo):
        cursor = self.conn.cursor()
        cursor.execute("SELECT nome, quantidade, quantidade_minima FROM estoque WHERE codigo=?", (codigo,))
        resultado = cursor.fetchone()
        if resultado:
            nome, quantidade, quantidade_minima = resultado
            if quantidade < quantidade_minima:
                print(f"ALERTA: O produto {nome} (Código: {codigo}) está abaixo do estoque mínimo! Quantidade atual: {quantidade}")

    def listar_produtos(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT nome, codigo, quantidade, categoria FROM estoque")
        produtos = cursor.fetchall()
        return produtos

    def calcular_estoque_por_categoria(self, categoria):
        cursor = self.conn.cursor()
        cursor.execute("SELECT SUM(quantidade) FROM estoque WHERE categoria=?", (categoria,))
        total = cursor.fetchone()[0]
        return total if total else 0

    def calcular_estoque_individual(self, codigo):
        return self.consultar_estoque(codigo)

class InterfaceCLI:
    def __init__(self, sistema):
        self.sistema = sistema

    def mostrar_menu(self):
        print("\n--- Sistema de Controle de Estoque ---")
        print("1. Adicionar Produto")
        print("2. Remover Produto")
        print("3. Consultar Estoque de um Produto")
        print("4. Listar Todos os Produtos")
        print("5. Calcular Estoque por Categoria")
        print("6. Sair")

    def executar(self):
        while True:
            self.mostrar_menu()
            escolha = input("Escolha uma opção: ")

            if escolha == "1":
                self.adicionar_produto()
            elif escolha == "2":
                self.remover_produto()
            elif escolha == "3":
                self.consultar_estoque()
            elif escolha == "4":
                self.listar_produtos()
            elif escolha == "5":
                self.calcular_estoque_por_categoria()
            elif escolha == "6":
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida. Tente novamente.")

    def adicionar_produto(self):
        print("\n--- Adicionar Produto ---")
        nome = input("Nome do produto: ")
        codigo = input("Código do produto: ")
        quantidade = int(input("Quantidade: "))
        quantidade_minima = int(input("Quantidade mínima: "))
        categoria = input("Categoria: ")
        self.sistema.adicionar_produto(nome, codigo, quantidade, quantidade_minima, categoria)
        print("Produto adicionado com sucesso!")

    def remover_produto(self):
        print("\n--- Remover Produto ---")
        codigo = input("Código do produto: ")
        quantidade = int(input("Quantidade a remover: "))
        self.sistema.remover_produto(codigo, quantidade)

    def consultar_estoque(self):
        print("\n--- Consultar Estoque ---")
        codigo = input("Código do produto: ")
        estoque = self.sistema.consultar_estoque(codigo)
        print(f"Estoque do produto: {estoque}")

    def listar_produtos(self):
        print("\n--- Lista de Produtos ---")
        produtos = self.sistema.listar_produtos()
        for produto in produtos:
            print(f"Nome: {produto[0]}, Código: {produto[1]}, Quantidade: {produto[2]}, Categoria: {produto[3]}")

    def calcular_estoque_por_categoria(self):
        print("\n--- Calcular Estoque por Categoria ---")
        categoria = input("Categoria: ")
        total = self.sistema.calcular_estoque_por_categoria(categoria)
        print(f"Estoque total da categoria {categoria}: {total}")

# Execução do código
sistema = Gestao("estoque.db")
interface = InterfaceCLI(sistema)
interface.executar()