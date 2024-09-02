def menu():
    OPTIONS = ('d', 'e', 's', 'q')
    invalid = True
    selected_option = ''

    print(f"""
    ======================================
    Pressione:
        [d] para depositar
        [e] para retirar o extrato
        [s] para realizar um saque
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


def deposit():
    invalid = True
    value = 0

    while invalid:
        value = float(input("==> Valor do depósito: "))
        invalid = value <= 0

        if(invalid):
            print("Valor informado deve ser positivo e diferente de zero!")

    return value
        

def withdrawal(account_total_sum):
    MAX_AMOUNT_PER_WITHDRAWAL = 500
    invalid = True
    value = 0

    while invalid:
        value = float(input("==> Valor do saque: "))

        exceded_total = value > account_total_sum
        exceded_max_value = value > MAX_AMOUNT_PER_WITHDRAWAL
        invalid_number = value <= 0
        invalid = exceded_max_value or exceded_total or invalid_number

        if(exceded_total):
            print("Você não tem dinheiro suficiente para realizar esse saque!")
        elif(exceded_max_value):
            print("O valor informado ultrapassa o limite do saque (R$ 500.00)")
        elif(invalid_number):
            print("O valor informado deve ser maior do que zero!")

    return value

def statement(transactions, money_sum):
    print(f"""
    ======================================
    Extrato detalhado:
    """)

    if(len(transactions) <= 0):
        print("    Nenhuma transação foi realizada!")
    else:
        for transaction in transactions:
            print(f"\t{transaction}")
    
    print(f"""
    Total na conta: {money_sum:.2f}
    ======================================
    """)


if __name__ == '__main__':
    MAX_WITHDRAWAL_PER_DAY = 3
    total_withdrawal_today = 0

    money_sum = 0
    transactions = []

    try:
        while True:
            selected_option = menu()

            if(selected_option == 'q'):
                quit_system()

            elif(selected_option == 'd'):
                value = deposit()
                transactions.append(f'+ R$ {value:.2f}')
                money_sum += value

            elif(selected_option == 's'):

                if(total_withdrawal_today < MAX_WITHDRAWAL_PER_DAY):
                    value = withdrawal(money_sum)
                    transactions.append(f'- R$ {value:.2f}')
                    money_sum -= value
                    total_withdrawal_today += 1
                else:
                    print("você atingiu o limite máximo de saques hoje. Por valor, volte amanhã!")
            
            else:
                statement(transactions, money_sum)

    except KeyboardInterrupt:
        quit_system()
    except Exception as error:
        print(f"Ocorreu um error: {str(error)}")
        quit_system()
