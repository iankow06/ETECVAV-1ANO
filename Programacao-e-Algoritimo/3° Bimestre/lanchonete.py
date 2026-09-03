import json
import os


# ============================================================
# CONFIGURAÇÕES
# ============================================================

ARQUIVO_DADOS = "lanchonete_dados.json"


# ============================================================
# FUNÇÕES DE ARQUIVO
# ============================================================

def carregar_dados():
    """
    Carrega os dados do arquivo JSON.
    Caso o arquivo não exista, cria uma estrutura vazia.
    """

    if not os.path.exists(ARQUIVO_DADOS):
        dados = {
            "produtos": [],
            "pedidos": []
        }

        salvar_dados(dados)
        return dados

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        return dados

    except (json.JSONDecodeError, OSError):
        print("\nErro ao ler o arquivo de dados.")
        print("Um novo arquivo será criado.\n")

        dados = {
            "produtos": [],
            "pedidos": []
        }

        salvar_dados(dados)

        return dados


def salvar_dados(dados):
    """
    Salva os dados no arquivo JSON.
    """

    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)


# ============================================================
# FUNÇÕES DE VALIDAÇÃO
# ============================================================

def ler_inteiro(mensagem):
    """
    Solicita um número inteiro ao usuário.
    """

    while True:
        try:
            valor = int(input(mensagem))
            return valor

        except ValueError:
            print("Digite um número inteiro válido.")


def ler_inteiro_positivo(mensagem):
    """
    Solicita um número inteiro maior que zero.
    """

    while True:
        valor = ler_inteiro(mensagem)

        if valor > 0:
            return valor

        print("Digite um número maior que zero.")


def ler_preco(mensagem):
    """
    Solicita um preço válido.
    Aceita vírgula ou ponto como separador decimal.
    """

    while True:
        entrada = input(mensagem).strip().replace(",", ".")

        try:
            preco = float(entrada)

            if preco >= 0:
                return preco

            print("O preço não pode ser negativo.")

        except ValueError:
            print("Digite um preço válido.")


def ler_nome(mensagem):
    """
    Solicita um nome que não esteja vazio.
    """

    while True:
        nome = input(mensagem).strip()

        if nome:
            return nome

        print("O campo não pode ficar vazio.")


# ============================================================
# PRODUTOS
# ============================================================

def cadastrar_produto(dados):
    """
    Cadastra um novo produto.
    """

    print("\n" + "=" * 50)
    print("             CADASTRAR PRODUTO")
    print("=" * 50)

    codigo = ler_inteiro_positivo("Código do produto: ")

    # Verifica se o código já existe
    for produto in dados["produtos"]:
        if produto["codigo"] == codigo:
            print("\nErro: já existe um produto com esse código.")
            return

    nome = ler_nome("Nome do produto: ")
    preco = ler_preco("Preço do produto: R$ ")
    estoque = ler_inteiro_positivo("Quantidade em estoque: ")

    produto = {
        "codigo": codigo,
        "nome": nome,
        "preco": preco,
        "estoque": estoque
    }

    dados["produtos"].append(produto)

    salvar_dados(dados)

    print("\nProduto cadastrado com sucesso!")


def listar_produtos(dados):
    """
    Exibe todos os produtos cadastrados.
    """

    print("\n" + "=" * 70)
    print("                    PRODUTOS CADASTRADOS")
    print("=" * 70)

    if len(dados["produtos"]) == 0:
        print("Nenhum produto cadastrado.")
        return

    for produto in dados["produtos"]:
        print(f"Código:    {produto['codigo']}")
        print(f"Nome:      {produto['nome']}")
        print(f"Preço:     R$ {produto['preco']:.2f}")
        print(f"Estoque:   {produto['estoque']} unidade(s)")
        print("-" * 70)


# ============================================================
# PEDIDOS
# ============================================================

def fazer_pedido(dados):
    """
    Registra um novo pedido.
    """

    print("\n" + "=" * 50)
    print("                 FAZER PEDIDO")
    print("=" * 50)

    # Verifica se existem produtos
    if len(dados["produtos"]) == 0:
        print("Não existem produtos cadastrados.")
        print("Cadastre um produto antes de realizar um pedido.")
        return

    nome_cliente = ler_nome("Nome do cliente: ")

    listar_produtos(dados)

    codigo = ler_inteiro_positivo("\nCódigo do produto: ")

    # Procura o produto
    produto_encontrado = None

    for produto in dados["produtos"]:
        if produto["codigo"] == codigo:
            produto_encontrado = produto
            break

    # Produto inexistente
    if produto_encontrado is None:
        print("\nErro: produto não encontrado.")
        return

    print(f"\nProduto selecionado: {produto_encontrado['nome']}")
    print(f"Preço unitário: R$ {produto_encontrado['preco']:.2f}")
    print(f"Estoque disponível: {produto_encontrado['estoque']}")

    quantidade = ler_inteiro_positivo("Quantidade desejada: ")

    # Verifica estoque
    if quantidade > produto_encontrado["estoque"]:
        print("\nErro: estoque insuficiente.")
        print(f"Estoque disponível: {produto_encontrado['estoque']}")
        return

    # Calcula o valor total
    valor_total = produto_encontrado["preco"] * quantidade

    # Atualiza o estoque
    produto_encontrado["estoque"] -= quantidade

    # Cria o pedido
    pedido = {
        "cliente": nome_cliente,
        "codigo_produto": produto_encontrado["codigo"],
        "nome_produto": produto_encontrado["nome"],
        "quantidade": quantidade,
        "valor_total": valor_total
    }

    dados["pedidos"].append(pedido)

    # Salva as alterações
    salvar_dados(dados)

    print("\n" + "=" * 50)
    print("             PEDIDO REALIZADO!")
    print("=" * 50)
    print(f"Cliente:       {nome_cliente}")
    print(f"Produto:       {produto_encontrado['nome']}")
    print(f"Quantidade:    {quantidade}")
    print(f"Valor total:   R$ {valor_total:.2f}")
    print("=" * 50)


def ver_pedidos(dados):
    """
    Exibe todos os pedidos realizados.
    """

    print("\n" + "=" * 70)
    print("                    PEDIDOS REALIZADOS")
    print("=" * 70)

    if len(dados["pedidos"]) == 0:
        print("Nenhum pedido realizado.")
        return

    total_vendas = 0

    for numero, pedido in enumerate(dados["pedidos"], start=1):

        print(f"\nPedido #{numero}")
        print(f"Cliente:          {pedido['cliente']}")
        print(f"Código produto:   {pedido['codigo_produto']}")
        print(f"Produto:          {pedido['nome_produto']}")
        print(f"Quantidade:       {pedido['quantidade']}")
        print(f"Valor total:      R$ {pedido['valor_total']:.2f}")

        print("-" * 70)

        total_vendas += pedido["valor_total"]

    print(f"\nTotal de vendas: R$ {total_vendas:.2f}")


# ============================================================
# MENU
# ============================================================

def exibir_menu():
    """
    Exibe o menu principal.
    """

    print("\n")
    print("=" * 50)
    print("             SISTEMA DA LANCHONETE")
    print("=" * 50)
    print("1 - Cadastrar produto")
    print("2 - Listar produtos")
    print("3 - Fazer pedido")
    print("4 - Ver pedidos realizados")
    print("5 - Sair")
    print("=" * 50)


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    # Carrega os dados quando o programa começa
    dados = carregar_dados()

    print("=" * 50)
    print("       BEM-VINDO AO SISTEMA DA LANCHONETE")
    print("=" * 50)

    while True:

        exibir_menu()

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_produto(dados)

        elif opcao == "2":
            listar_produtos(dados)

        elif opcao == "3":
            fazer_pedido(dados)

        elif opcao == "4":
            ver_pedidos(dados)

        elif opcao == "5":
            print("\nEncerrando o sistema...")
            print("Obrigado por utilizar o sistema da lanchonete!")
            break

        else:
            print("\nOpção inválida. Escolha uma opção de 1 a 5.")


# ============================================================
# INÍCIO DO PROGRAMA
# ============================================================

if __name__ == "__main__":
    main()