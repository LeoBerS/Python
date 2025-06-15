from datetime import date
from abc import ABC, abstractmethod

# =========================
# Classe base Cliente
# =========================
class Cliente:
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas = []  # Lista de contas associadas ao cliente

    def adicionar_conta(self, conta):
        self.contas.append(conta)

# =========================
# Subclasse PessoaFisica
# =========================
class PessoaFisica(Cliente):
    def __init__(self, nome: str, cpf: str, data_nascimento: date, endereco: str):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

# =========================
# Classe Historico de transações
# =========================
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

# =========================
# Classe base Conta
# =========================
class Conta:
    def __init__(self, numero: int, agencia: str, cliente):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero: int, agencia: str = "0001"):
        return cls(numero=numero, agencia=agencia, cliente=cliente)

    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            print("Valor de saque deve ser positivo.")
            return False
        if valor > self.saldo:
            print("Saldo insuficiente.")
            return False
        self.saldo -= valor
        return True

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print("Valor de depósito deve ser positivo.")
            return False
        self.saldo += valor
        return True

# =========================
# Subclasse ContaCorrente
# =========================
class ContaCorrente(Conta):
    def __init__(self, numero: int, agencia: str, cliente, limite: float = 500.0, limite_saques: int = 3):
        super().__init__(numero, agencia, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = 0

    def sacar(self, valor: float) -> bool:
        if self.saques_realizados >= self.limite_saques:
            print("Limite de saques diários atingido.")
            return False
        if valor > self.limite:
            print(f"Valor excede o limite de R$ {self.limite:.2f} por saque.")
            return False
        if super().sacar(valor):
            self.saques_realizados += 1
            return True
        return False

# =========================
# Interface Transacao
# =========================
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta: Conta):
        pass

# =========================
# Classe Deposito
# =========================
class Deposito(Transacao):
    def __init__(self, valor: float):
        self.valor = valor

    def registrar(self, conta: Conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)

# =========================
# Classe Saque
# =========================
class Saque(Transacao):
    def __init__(self, valor: float):
        self.valor = valor

    def registrar(self, conta: Conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)

# =========================
# Funções auxiliares e menu
# =========================
clientes = []
contas = []

def localizar_cliente_por_cpf(cpf):
    for cliente in clientes:
        if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf:
            return cliente
    return None

def menu():
    print("=== Bem-vindo ao Sistema Bancário ===")

    while True:
        print("\n--- Menu ---")
        print("1. Depositar")
        print("2. Sacar")
        print("3. Extrato")
        print("4. Abrir nova Conta")
        print("5. Listar contas")
        print("6. Criar novo Cliente")
        print("7. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cpf = input("Informe o CPF do cliente: ")
            cliente = localizar_cliente_por_cpf(cpf)
            if not cliente:
                print("Cliente não encontrado.")
                continue
            conta = cliente.contas[0] if cliente.contas else None
            if not conta:
                print("Cliente não possui conta.")
                continue
            valor = float(input("Valor do depósito: "))
            transacao = Deposito(valor)
            transacao.registrar(conta)

        elif opcao == "2":
            cpf = input("Informe o CPF do cliente: ")
            cliente = localizar_cliente_por_cpf(cpf)
            if not cliente:
                print("Cliente não encontrado.")
                continue
            conta = cliente.contas[0] if cliente.contas else None
            if not conta:
                print("Cliente não possui conta.")
                continue
            valor = float(input("Valor do saque: "))
            transacao = Saque(valor)
            transacao.registrar(conta)

        elif opcao == "3":
            cpf = input("Informe o CPF do cliente: ")
            cliente = localizar_cliente_por_cpf(cpf)
            if not cliente:
                print("Cliente não encontrado.")
                continue
            conta = cliente.contas[0] if cliente.contas else None
            if not conta:
                print("Cliente não possui conta.")
                continue
            print("\n=== Extrato ===")
            for t in conta.historico.transacoes:
                tipo = t.__class__.__name__
                print(f"{tipo}: R$ {t.valor:.2f}")
            print(f"Saldo atual: R$ {conta.saldo:.2f}")

        elif opcao == "4":
            cpf = input("Informe o CPF do cliente: ")
            cliente = localizar_cliente_por_cpf(cpf)
            if not cliente:
                print("Cliente não encontrado.")
                continue
            numero = len(contas) + 1
            conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero)
            cliente.adicionar_conta(conta)
            contas.append(conta)
            print(f"Conta {numero} criada com sucesso.")

        elif opcao == "5":
            for conta in contas:
                print(f"Agência: {conta.agencia} | Número: {conta.numero} | Cliente: {conta.cliente.nome}")

        elif opcao == "6":
            nome = input("Nome: ")
            cpf = input("CPF: ")
            data_nascimento = input("Data de nascimento (AAAA-MM-DD): ")
            endereco = input("Endereço: ")
            cliente = PessoaFisica(
                nome=nome,
                cpf=cpf,
                data_nascimento=date.fromisoformat(data_nascimento),
                endereco=endereco
            )
            clientes.append(cliente)
            print("Cliente criado com sucesso.")

        elif opcao == "7":
            print("Encerrando o sistema. Até logo!")
            break

        else:
            print("Opção inválida. Tente novamente.")

# Descomente a linha abaixo para executar o menu interativo
# menu()
