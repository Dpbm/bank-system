def menu():
    OPTIONS = ('d', 'e', 's', 'q', 'nu', 'na', 'la')
    invalid = True
    selected_option = ''

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
    
    while invalid:    
        selected_option = input("==> ")
        invalid = selected_option not in OPTIONS

        if(invalid):
            print("Opção inválida. Por favor, tente novamente!")
    
    return selected_option

def quit_system():
    import sys 
    print("Obrigado por utilizar nosso sistema!")    
    sys.exit(0)

def update_history(history, text):
    history.append(text)

def deposit(value, amount, history, /):
    if(value <= 0):
       print("Valor informado deve ser positivo e diferente de zero!")
       return amount

    update_history(history, f'+ R$ {value:.2f}')
    return amount + value

def withdrawal(*, value, amount, max_amount, max_withdrawals_per_day, total_withdrawal_today, history):
    exceded_total = value > amount
    exceded_max_value = value > max_amount
    exceded_withdrawals_per_day = total_withdrawal_today >= max_withdrawals_per_day
    invalid_number = value <= 0
    invalid = exceded_max_value or exceded_total or invalid_number or exceded_withdrawals_per_day
    
    if(exceded_total):
        print("Você não tem dinheiro suficiente para realizar esse saque!")
    if(exceded_max_value):
        print(f"O valor informado ultrapassa o limite do saque (R$ {max_amount:.2f})")
    if(invalid_number):
        print("O valor informado deve ser maior do que zero!")
    if(exceded_withdrawals_per_day):
        print(f"Você ultrapassou o maximo de saques hoje (maximo {max_withdrawals_per_day} por dia)!")

    if(invalid):
       return (amount, total_withdrawal_today)

    update_history(history, f'- R$ {value:.2f}')
    return (amount-value, total_withdrawal_today+1) 

def statement(amount, /, *, history):
    print(f"""
    ======================================
    Extrato detalhado:
    """)

    if(len(history) <= 0):
        print("    Nenhuma transação foi realizada!")
    else:
        for transaction in history:
            print(f"\t{transaction}")
    
    print(f"""
    Total na conta: {amount:.2f}
    ======================================
    """)

def get_user(users, cpf):
    users_found = [user for user in users if user['cpf'] == cpf]
    return users_found[0] if len(users_found)>0 else None

def create_user(users):
    cpf = input("==> CPF: ")

    if(get_user(users, cpf) is not None):
        print("Usuário já cadastrado!")
        return

    name = input("==> Nome: ")
    birth = input("==> Data de nascimento (dd-mm-aaaa): ")
    address = input("==> Endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    users.append({'cpf':cpf, 'name':name, 'birth':birth, 'address':address})

    print("Usuário criado com sucesso")

def create_account(agency, account_number, users, accounts):
    cpf = input("==> Informe o CPF: ")

    user = get_user(users, cpf)
    if(user is None):
        print("Usuário não existe!")
        return

    accounts.append({"agency":agency, "account_number":account_number, 'cpf':cpf})

def list_accounts(users, accounts):
    
    if(len(accounts) <= 0):
        print("Nenhuma conta foi adicionada!")
        return

    print("\nContas:")
    for account in accounts:
        print('*'*50)
        print(f"Agência: {account['agency']}")
        print(f"Número da conta: {account['account_number']}")
        user = get_user(users, account['cpf'])
        print(f"Titular: {user['name']}")
        print('*'*50)

if __name__ == '__main__':
    MAX_WITHDRAWAL_PER_DAY = 3
    MAX_WITHDRAWAL_VALUE = 500
    total_withdrawal_today = 0
    
    AGENCY = '0001'

    users = []
    accounts = []

    amount = 0
    transactions = []

    try:
        while True:
            selected_option = menu()

            if(selected_option == 'q'):
                quit_system()

            elif(selected_option == 'd'):
                value = float(input("==> Valor do depósito: ")) 
                amount = deposit(value, amount, transactions)

            elif(selected_option == 's'):
                value = float(input("==> Valor do saque: "))        
                amount, total_withdrawal_today = withdrawal(
                    value=value,
                    amount=amount,
                    max_amount=MAX_WITHDRAWAL_VALUE,
                    max_withdrawals_per_day=MAX_WITHDRAWAL_PER_DAY,
                    total_withdrawal_today=total_withdrawal_today,
                    history=transactions,
                )
            
            elif(selected_option == 'nu'):
                create_user(users)

            elif(selected_option == 'na'):
                account_number = len(accounts)+1
                create_account(AGENCY, account_number, users, accounts)

            elif(selected_option == 'la'):
                list_accounts(users, accounts)

            else:
                statement(amount, history=transactions)

    except KeyboardInterrupt:
        quit_system()
    except Exception as error:
        print(f"Ocorreu um erro: {str(error)}")
        quit_system()
