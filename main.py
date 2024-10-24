import datetime
from abc import ABC, abstractmethod
from typing import Tuple


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
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
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)

    def sacar(self, valor):
        saldo = self.saldo

        if valor > saldo:
            print("Operação falhou. Não há saldo sufuciente.")

        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso.")
            return True

        else:
            print("Operação falhou. Valor informado é inválido.")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso.")
            return True

        else:
            print("Operação falhou. Valor informado é inválido.")

        return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [
                transacao
                for transacao in self.historico.transacoes
                if transacao["tipo"] == Saque.__name__
            ]
        )

        if valor > self.limite:
            print("Operação falhou. O valor do saque excede o limite.")

        elif numero_saques >= self.limite_saques:
            print("Operação falhou. O número de saques diário máximo foi excedido.")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
                Agência:\t{self.agencia}
                C/C:\t\t{self.numero}
                Titular:\t{self.cliente.nome}
                """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


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


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


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
