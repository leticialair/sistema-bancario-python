from typing import Tuple

extrato = ""
valor_saldo = 0
contagem_saque = 0


class OperacoesBancarias:

    def __init__(self, valor_limite_saque: float = 500, contagem_limite_saque: int = 3):
        self.valor_limite_saque = valor_limite_saque
        self.contagem_limite_saque = contagem_limite_saque

    def exibir_menu(self) -> str:
        return """
                Digite a letra da operação desejada:

                [d] Depósito
                [s] Saque
                [e] Extrato
                [q] Sair do sistema

                ==> """

    def depositar(
        self, extrato: str, valor_saldo: float, valor: float
    ) -> Tuple[str, float]:
        if valor > 0:
            extrato += f"Depósito: R$ {valor:.2f}\n"
            valor_saldo += valor

        else:
            print("Valor informado é inválido.")

        return (extrato, valor_saldo)

    def sacar(
        self, extrato: str, valor_saldo: float, contagem_saque: int, valor: float
    ) -> Tuple[str, float, int]:
        if valor > valor_saldo:
            print("Não há saldo suficiente para o saque solicitado.")

        elif valor > self.valor_limite_saque:
            print("O valor do saque excede o limite máximo permitido.")

        elif contagem_saque > self.contagem_limite_saque:
            print(
                "O limite diário de saques já foi atingido. Tente novamente no dia seguinte."
            )

        elif valor > 0:
            extrato += f"Saque: R$ {valor:.2f}\n"
            valor_saldo -= valor
            contagem_saque += 1

        else:
            print("Valor informado é inválido.")

        return (extrato, valor_saldo, contagem_saque)

    def imprimir_extrato(extrato: str, valor_saldo: float) -> None:
        print("============== EXTRATO ==============\n")
        if extrato is None:
            print("Não foram realizadas movimentações.\n")
        else:
            print(f"{extrato}\n")
        print(f"Saldo: R$ {valor_saldo:.2f}.\n")
        print("=====================================")

        return


while True:

    opcao = input(OperacoesBancarias().exibir_menu())

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))
        extrato, valor_saldo = OperacoesBancarias().depositar(
            extrato, valor_saldo, valor
        )

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))
        extrato, valor_saldo, contagem_saque = OperacoesBancarias().sacar(
            extrato, valor_saldo, contagem_saque, valor
        )

    elif opcao == "e":
        OperacoesBancarias().imprimir_extrato(extrato, valor_saldo)

    elif opcao == "q":
        break

    else:
        print("Letra da operação é inválida.")
