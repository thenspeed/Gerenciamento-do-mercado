import csv
import os

# Lista de tipos de clientes
lista_Dados_clientes = ['CPF', 'nome', 'data de nascimento', 'idade', 'endereco', 'cidade', 'estado', 'pontos']

# Função para verificar se um cliente já está cadastrado
def verificar_cliente_existe(cpf):
    # Verifica se o arquivo existe
    arquivo_existe = os.path.exists('clientes.csv')

    # Se o arquivo não existir, cria o arquivo e escreve o cabeçalho
    if not arquivo_existe:
        with open('clientes.csv', 'a', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            escritor.writerow(lista_Dados_clientes)

    try:
        # Abre o arquivo CSV e procura pelo cliente
        with open('clientes.csv', 'r', encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo)
            for linha in leitor:
                if linha['CPF'] == cpf:
                    return linha
            return None
    except FileNotFoundError:
        # Se o arquivo não for encontrado, retorne None
        return None

# Função para incluir um novo cliente
def incluir_cliente():
    lista_pessoa = {}
    lista_pessoa['CPF'] = input("Digite o seu CPF: \n ")
    os.system('cls') or None
    existe = verificar_cliente_existe(lista_pessoa['CPF'])
    if existe is not None:
        print("CPF já cadastrado:")
        for chave, valor in existe.items():
             if chave != 'data de nascimento':
                 print(f'{chave}: {valor}')
             else:
                valor = eval(valor)
                valor_formartado = '/'.join(valor)
                print(f'{chave}: {valor_formartado}')
        input("Pressione Enter para continuar...")
        os.system('cls')
        return
    else:
        os.system('cls') or None
        lista_pessoa['nome'] = input("Digite o seu Nome: \n ")
        os.system('cls') or None
        lista_data_nascimento = ['dia', 'mês', 'ano']
        for i in range(3):
            lista_data_nascimento[i] = input(f"Digite o {lista_data_nascimento[i]} da data em que nasceu: \n ")
            os.system('cls') or None
        lista_pessoa['data de nascimento'] = lista_data_nascimento
        lista_pessoa['idade'] = input("Digite a sua idade: \n ")
        os.system('cls') or None
        lista_pessoa['endereco'] = input("Digite seu endereço: \n ")
        os.system('cls') or None
        lista_pessoa['cidade'] = input("Digite o nome da cidade onde nasceu: \n ")
        os.system('cls') or None
        lista_pessoa['estado'] = input("Digite a sigla do Estado onde nasceu: \n ")
        os.system('cls') or None
        lista_pessoa['pontos'] = 0
        with open('clientes.csv', 'a', newline='') as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(lista_pessoa.values())
        return

def alterar_cliente():
    # Solicita ao usuário o CPF do cliente a ser alterado
    cpf = input('Digite o CPF do cliente que deseja alterar: ')

    # Verifica se o cliente existe
    cliente_existente = verificar_cliente_existe(cpf)

    # Se o cliente não existir, exibe uma mensagem e retorna
    if cliente_existente is None:
        print('Cliente não encontrado.')
        return

    # Exibe as informações do cliente
    print('Informações do cliente:')
    cont = 1
    for chave, valor in cliente_existente.items():
        if chave != 'data de nascimento':
            print(f'{cont}: {chave} {valor}')
            cont += 1
        else:
            valor = eval(valor)
            valor_formartado = '/'.join(valor)
            print(f'{cont}: {chave} {valor_formartado}')
            cont += 1

    # Solicita ao usuário a opção que deseja alterar
    opcao = int(input('Digite o número da opção que deseja alterar: ')) - 1

    if opcao == 2:  # Se for alterar a data de nascimento
        lista_data_nascimento = []
        for campo in ['dia', 'mês', 'ano']:
            novo_valor = input(f'Digite o novo valor para {campo}: ')
            lista_data_nascimento.append(novo_valor)
        valor = lista_data_nascimento
    elif opcao == 7:  # Se for alterar os pontos
        valor = int(input('Digite o valor a ser atribuído: '))
    else:
        valor = input('Digite o valor a ser atribuído: ')

    # Atualiza os dados do cliente
    cliente_existente[lista_Dados_clientes[opcao]] = valor

    # Lê todas as linhas do arquivo CSV
    with open('clientes.csv', 'r', newline='') as arquivo:
        leitor = csv.DictReader(arquivo)
        linhas = list(leitor)

    # Atualiza os dados do cliente na lista de linhas
    for i, linha in enumerate(linhas):
        if linha['CPF'] == cpf:
            linhas[i] = cliente_existente

    # Escreve as alterações no arquivo CSV
    with open('clientes.csv', 'w', newline='') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=lista_Dados_clientes)
        escritor.writeheader()
        escritor.writerows(linhas)

    print('Cliente alterado com sucesso.')
    os.system('cls') or None
    return

# Função principal para exibir o painel do cliente
def painel_cliente():
    resp = input("""
        1 = Cadastrar cliente
        2 = Alterar cliente
        3 = Voltar
    """)
    os.system('cls') or None
    if resp == '1':
        incluir_cliente()
    elif resp == '2':
        alterar_cliente()
    elif resp == '3':
        return
    else:
        return painel_cliente()


