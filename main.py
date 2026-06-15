from app.sistema import SistemaDeEmprestimos


def main():
    sistema = SistemaDeEmprestimos()

    while True:
        print("\n1-Registrar 2-Devolver 3-Atrasados 0-Sair")
        opcao = input("Opção: ")

        if opcao == "1":
            sistema.registrar(
                int(input("ID equipamento: ")),
                input("Nome: "),
                input("Email: "),
                int(input("Dias: "))
            )

        elif opcao == "2":
            sistema.devolver(int(input("ID empréstimo: ")))

        elif opcao == "3":
            sistema.listar_atrasados()

        elif opcao == "0":
            break


if __name__ == "__main__":
    main()