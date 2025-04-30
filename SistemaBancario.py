from decimal import Decimal, InvalidOperation

class ContaBancaria:
    def __init__(self):
        self.saldo = Decimal('0.0')  # Inicializa o saldo da conta com 0.0
        self.depositos = []  # Lista para armazenar todos os depósitos
        self.saques = []  # Lista para armazenar todos os saques
        self.saques_diarios = 0  # Contador para limitar o número de saques diários

    def depositar(self, valor):
        try:
            valor = Decimal(valor)
            # Verifica se o valor tem até duas casas decimais
            if valor.as_tuple().exponent < -2:
                raise InvalidOperation
            if valor > 0:  # Verifica se o valor do depósito é positivo
                self.saldo += valor  # Adiciona o valor ao saldo
                self.depositos.append(valor)  # Armazena o depósito na lista de depósitos
                print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")  # Confirma o depósito
            else:
                print("Valor de depósito deve ser positivo.")  # Mensagem de erro para valores negativos
        except InvalidOperation:
            print("Só números decimais no formato xxxx.xx são aceitos.")  # Mensagem de erro para valores inválidos

    def sacar(self, valor):
        try:
            valor = Decimal(valor)
            # Verifica se o valor tem até duas casas decimais
            if valor.as_tuple().exponent < -2:
                raise InvalidOperation
            if valor <= 0:  # Verifica se o valor do saque é positivo
                print("Valor de saque deve ser positivo.")  # Mensagem de erro para valores negativos
            elif self.saques_diarios >= 3:  # Verifica se o limite diário de saques foi atingido
                print("Limite diário de saques atingido.")  # Mensagem de erro para limite de saques
            elif valor > 500:  # Verifica se o valor do saque é maior que o limite permitido
                print("Limite máximo por saque é de R$ 500,00.")  # Mensagem de erro para valor de saque
            elif valor > self.saldo:  # Verifica se há saldo suficiente para o saque
                print("Saldo insuficiente para realizar o saque.")  # Mensagem de erro para saldo insuficiente
            else:
                self.saldo -= valor  # Subtrai o valor do saldo
                self.saques.append(valor)  # Armazena o saque na lista de saques
                self.saques_diarios += 1  # Incrementa o contador de saques diários
                print(f"Saque de R$ {valor:.2f} realizado com sucesso.")  # Confirma o saque
        except InvalidOperation:
            print("Só números decimais no formato xxxx.xx são aceitos.")  # Mensagem de erro para valores inválidos
    def extrato(self):
        if not self.depositos and not self.saques:  # Verifica se não houve movimentações
            print("Não foram realizadas movimentações.")  # Mensagem para extrato vazio
        else:
            print("Extrato:")  # Título do extrato
            for deposito in self.depositos:  # Itera sobre a lista de depósitos
                print(f"Depósito: R$ {deposito:.2f}")  # Exibe cada depósito
            for saque in self.saques:  # Itera sobre a lista de saques
                print(f"Saque: R$ {saque:.2f}")  # Exibe cada saque
            print(f"Saldo atual: R$ {self.saldo:.2f}")  # Exibe o saldo atual

# Função para exibir o menu e processar as opções do usuário
def menu():
    conta = ContaBancaria()  # Cria uma nova instância da classe ContaBancaria
    
    while True:
        print("\nMenu:")  # Exibe o menu de opções
        print("1. Depósito")  # Opção de depósito
        print("2. Saque")  # Opção de saque
        print("3. Extrato")  # Opção de extrato
        print("4. Sair")  # Opção de sair
        
        opcao = input("Escolha uma opção: ")  # Solicita ao usuário que escolha uma opção
        
        if opcao == '1':
            valor = input("Digite o valor do depósito: ")  # Solicita o valor do depósito
            conta.depositar(valor)  # Chama o método depositar
        elif opcao == '2':
            valor = input("Digite o valor do saque: ")  # Solicita o valor do saque
            conta.sacar(valor)  # Chama o método sacar
        elif opcao == '3':
            conta.extrato()  # Chama o método extrato
        elif opcao == '4':
            print("Saindo do sistema. Até mais!")  # Mensagem de saída
            break  # Encerra o loop e sai do programa
        else:
            print("Opção inválida. Tente novamente.")  # Mensagem para opção inválida

# Executar o menu
menu()  # Chama a função menu para iniciar o programa
