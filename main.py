from typing import Tuple

# Definindo valores iniciais
extrato = ""
valor_saldo = 0
contagem_saque = 0
dict_usuarios = {}
dict_contas = {}
agencia = "001"


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
                [u] Criar usuário
                [c] Criar conta
                [q] Sair do sistema

                ==> """

    def depositar(
        self, extrato: str, valor_saldo: float, valor: float, /
    ) -> Tuple[str, float]:
        if valor > 0:
            extrato += f"Depósito: R$ {valor:.2f}\n"
            valor_saldo += valor

        else:
            print("Valor informado é inválido.")

        return (extrato, valor_saldo)

    def sacar(
        self, *, extrato: str, valor_saldo: float, contagem_saque: int, valor: float
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

    def imprimir_extrato(self, extrato: str, /, *, valor_saldo: float) -> None:
        print("============== EXTRATO ==============\n")
        if extrato is None:
            print("Não foram realizadas movimentações.\n")
        else:
            print(f"{extrato}\n")
        print(f"Saldo: R$ {valor_saldo:.2f}.\n")
        print("=====================================")

        return

    def criar_usuario(self, cpf: str, dict_usuarios: dict) -> dict:
        if cpf in dict_usuarios.keys():
            print("Esse CPF já possui um usuário associado.")

        else:
            nome = input("Digite seu nome completo: ")
            data_nascimento = input(
                "Digite sua data de nascimento (formato 01/01/1900): "
            )
            endereco = input("Digite seu endereço: ")

            dict_usuarios[cpf] = {
                "nome": nome,
                "data_nascimento": data_nascimento,
                "endereco": endereco,
            }

        return dict_usuarios

    def criar_conta(
        self,
        cpf: str,
        dict_usuarios: dict,
        dict_contas: dict,
        agencia: str,
        numero_conta: str,
    ) -> Tuple[dict, dict]:
        if cpf not in dict_usuarios.keys():
            print("Usuário não cadastrado. Favor cadastrar antes de abrir a conta.")

        else:
            dict_contas[cpf] = {"agencia": agencia, "numero_conta": numero_conta}

        return (dict_usuarios, dict_contas)


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
            extrato=extrato,
            valor_saldo=valor_saldo,
            contagem_saque=contagem_saque,
            valor=valor,
        )

    elif opcao == "e":
        OperacoesBancarias().imprimir_extrato(extrato, valor_saldo=valor_saldo)

    elif opcao == "u":
        cpf = input("Digite seu CPF (apenas números): ")
        dict_usuarios = OperacoesBancarias().criar_usuario(cpf, dict_usuarios)

    elif opcao == "c":
        cpf = input("Digite seu CPF (apenas números): ")
        numero_conta = len(dict_contas.keys()) + 1
        dict_usuarios, dict_contas = OperacoesBancarias().criar_conta(
            cpf, dict_usuarios, dict_contas, agencia, numero_conta
        )

    elif opcao == "q":
        break

    else:
        print("Letra da operação é inválida.")
