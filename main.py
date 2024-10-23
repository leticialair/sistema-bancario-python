class OperacoesBancarias:

    def __init__(self):
        pass

    def exibir_menu(self):
        return """
                Digite a letra da operação desejada:

                [d] Depósito
                [s] Saque
                [e] Extrato
                [q] Sair do sistema

                ==> """


extrato = ""
valor_saldo = 0
contagem_saque = 0

VALOR_LIMITE_SAQUE = 500
CONTAGEM_LIMITE_SAQUE = 3

while True:

    opcao = input(OperacoesBancarias().exibir_menu())

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            valor_saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"

        else:
            print("Valor informado é inválido.")

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))

        if valor > valor_saldo:
            print("Não há saldo suficiente para o saque solicitado.")

        elif valor > VALOR_LIMITE_SAQUE:
            print("O valor do saque excede o limite máximo permitido.")

        elif contagem_saque > CONTAGEM_LIMITE_SAQUE:
            print(
                "O limite diário de saques já foi atingido. Tente novamente no dia seguinte."
            )

        elif valor > 0:
            valor_saldo -= valor
            contagem_saque += 1
            extrato += f"Saque: R$ {valor:.2f}\n"

        else:
            print("Valor informado é inválido.")

    elif opcao == "e":
        print("============== EXTRATO ==============\n")
        if extrato is None:
            print("Não foram realzadas movimentações.\n")
        else:
            print(f"{extrato}\n")
        print(f"Saldo: R$ {valor_saldo:.2f}.\n")
        print("=====================================")

    elif opcao == "q":
        break

    else:
        print("Letra da operação é inválida.")
