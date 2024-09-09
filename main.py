from datetime import datetime
from abc import ABC, abstractmethod, abstractproperty

class Historico:
    def __init__(self):
        self._transacoes = []
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append({
                    "tipo":transacao.__class__.__name__,
                    "valor": transacao.valor,
                    "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s") 
                })

    @property
    def transacoes(self):
        return self._transacoes

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def historico(self):
        return self._historico

    @property
    def cliente(self):
        return self._cliente

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    def sacar(self, valor):
        if(self.saldo < valor):
            print("Você não tem dinheiro suficiente para realizar esse saque!")
            return False
        elif(valor <= 0):
            print("O valor informado deve ser maior do que zero!")
            return False

        self._saldo -= valor
        return True

    def depositar(self, valor):
        if(valor <= 0):
            print("Valor informado deve ser positivo e diferente de zero!")
            return False
        
        self._saldo += valor
        return True

    def __str__(self):
        return f"""
            Conta: {self.numero}
            Saldo: {self.saldo}
            Agência: {self.agencia}
            Titular: {self.cliente.nome}
        """

class ContaCorrente(Conta):
    def __init__(self, numero, cliente):
        super().__init__(numero, cliente)
        self._limite = 500
        self._limite_saques = 3
    
    def sacar(self, valor):
        total_transacoes = sum([
            1 for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__
        ])

        if(valor > self._limite):
            print("Esse valor ultrapassa o limite maximo por transação")
            return False
        elif (total_transacoes > self._limite_saques):
            print("Você atingiu o valor máximo de saques hoje")
            return False

        return super().sacar(valor)


class Transacao(ABC): 
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

    @property
    def contas(self):
        return self._contas

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self._cpf

    @property
    def nome(self):
        return self._nome

    @property
    def data_nascimento(self):
        return self._data_nascimento

    @property
    def endereco(self):
        return self._endereco

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        
        if(sucesso):
            conta.historico.adicionar_transacao(self)

    

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        
        if(sucesso):
            conta.historico.adicionar_transacao(self)

def menu():
    OPCOES = ('d', 'e', 's', 'q', 'nu', 'na', 'la')
    invalido = True
    opcao_selecionada = ''

    print(f"""
    ======================================
    Pressione:
        [d]  para depositar
        [e]  para retirar o extrato
        [s]  para realizar um saque
        [nu] criar novo usuário
        [na] criar nova conta
        [la] listar contas
        [q] para sair
    ======================================
    """)
    
    while invalido:    
        opcao_selecionada = input("==> ")
        invalido = opcao_selecionada not in OPCOES

        if(invalido):
            print("Opção inválida. Por favor, tente novamente!")
    
    return opcao_selecionada

def sair():
    import sys 
    print("Obrigado por utilizar nosso sistema!")    
    sys.exit(0)

def depositar(clientes):
    cpf = input("==> informe o cpf: ")

    cliente = [c for c in clientes if c.cpf == cpf]
    if(len(cliente) <= 0):
        print("Cliente inexistente")
        return
    cliente = cliente[0]

    valor = float(input("==> informe o valor do deposito: "))
     
    if(len(cliente.contas) <= 0):
        print("Este cliente não possui nenhuma conta asssociada")
        return

    conta = cliente.contas[0]

    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("==> informe o cpf: ")

    cliente = [c for c in clientes if c.cpf == cpf]
    if(len(cliente) <= 0):
        print("Cliente inexistente")
        return
    cliente = cliente[0]
    valor = float(input("==> informe o valor do saque: "))

    if(not cliente.contas):
        print("Este cliente não possui nenhuma conta associada")
        return

    conta = cliente.contas[0]

    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)

def crirar_cliente(clientes):
    cpf = input("==> CPF: ")

    mesmo_cpf = len([1 for cliente in clientes if cliente.cpf]) >= 1

    if(mesmo_cpf):
        print("Usuário já cadastrado!")
        return

    nome = input("==> Nome: ")
    data_nascimento = input("==> Data de nascimento (dd-mm-aaaa): ")
    endereco = input("==> Endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    cliente = PessoaFisica(cpf, nome, data_nascimento, endereco)
    clientes.append(cliente)

    print("Usuário criado com sucesso")

def criar_conta(numero, clientes, contas):
    cpf = input("==> Informe o CPF: ")

    cliente = [cliente for cliente in clientes if cliente.cpf == cpf]
    cliente_existe = len(cliente)>=1

    if(not cliente_existe):
        print("Usuário não existe!")
        return

    cliente = cliente[0]

    conta = ContaCorrente.nova_conta(cliente, numero)
    cliente.adicionar_conta(conta)
    contas.append(conta)

    print("Conta criada com sucesso")

def listar_contas(contas):
    
    if(len(contas) <= 0):
        print("Nenhuma conta foi adicionada!")
        return

    print("\nContas:")
    for conta in contas:
        print('*'*50)
        print(conta)
        print('*'*50)

def extrato(clientes):
    cpf = input("==> Informe o CPF: ")

    cliente = [cliente for cliente in clientes if cliente.cpf == cpf]
    cliente_existe = len(cliente)>=1

    if(not cliente_existe):
        print("Usuário não existe!")
        return

    cliente = cliente[0]
    
    if(len(cliente.contas) <= 0):
        print("Usuário não possui nenhuma conta associada")
        return

    conta = cliente.contas[0]
    transacoes = conta.historico.transacoes

    print(f"""
    ======================================
    Extrato detalhado:
    """)

    if(len(transacoes) <= 0):
        print("    Nenhuma transação foi realizada!")
    else:
        for transacao in transacoes:
            symbol = "+" if transacao['tipo'] == 'Deposito' else "-"
            print(f"\t{symbol} R$ {transacao['valor']:.2f}")
    
    print(f"""
    Total na conta: {conta.saldo:.2f}
    ======================================
    """)

if __name__ == '__main__':

    clientes = []
    contas = []

    try:
        while True:
            opcao = menu()

            if(opcao == 'q'):
                sair()

            elif(opcao == 'd'):
                depositar(clientes)

            elif(opcao == 's'):
                sacar(clientes)
            
            elif(opcao == 'nu'):
                crirar_cliente(clientes)

            elif(opcao == 'na'):
                numero = len(contas)+1
                criar_conta(numero, clientes, contas)

            elif(opcao == 'la'):
                listar_contas(contas)

            else:
                extrato(clientes)

    except KeyboardInterrupt:
        sair()
    except Exception as error:
        print(f"Ocorreu um erro: {str(error)}")
        sair()
