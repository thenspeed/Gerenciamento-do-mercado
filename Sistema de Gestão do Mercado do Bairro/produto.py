import csv
import os

# Função para gerar ID do produto
def gerador_Id_produto():
    try:
        contador = 0
        with open('produtos.csv', 'r', encoding='utf8', newline='') as arquivo:
            leitor = csv.DictReader(arquivo)
            for x in leitor:
                contador += 1
            
        return contador + 1  
    except FileNotFoundError:
        return 1  


# Função para incluir um novo produto
def incluir_produto():
    # Gera o ID do produto
    id = gerador_Id_produto()
    # Cria um dicionário para armazenar os detalhes do produto
    lista_produto = {'ID': id}
    # Obtém detalhes do produto do usuário
    setor = input("""Digite o número correspondente ao setor do produto:
                1: Higiene 
                2: Limpeza 
                3: Bebidas
                4: Frios
                5: Padaria
                6: Açougue 
                  """)
    os.system('cls') or None
    lista_produto['setor'] = setor
    lista_produto['nome'] = input("Digite o nome do produto:\n ")
    os.system('cls') or None
    lista_produto['preco'] = "{:.2f}".format(round(float(input("Digite o preço: \n ")), 2))
    os.system('cls') or None
    lista_data_validade = ['dia', 'mês', 'ano']
    for i in range(3):
        lista_data_validade[i] = input(f"Digite o {lista_data_validade[i]} da data de validade do produto: \n ")
        os.system('cls') or None   
    lista_produto['data de validade'] = lista_data_validade
    lista_produto['quantidade em estoque'] = int(input("Digite a quantidade desse produto em estoque: \n "))
    os.system('cls') or None

    # Exibe os detalhes do produto inserido
    for chave, valor in lista_produto.items():
            if chave != 'data de validade':
                print(f'{chave}: {valor}')
            else:
                valor_formartado = '/'.join(valor)
                print(f'{chave}: {valor_formartado}')
    input('')
    os.system('cls') or None
    # Abre o arquivo CSV em modo de adição e escreve os detalhes do produto
    with open('produtos.csv', 'a', newline='', encoding='utf8') as arquivo:
        escritor = csv.writer(arquivo)
        if arquivo.tell() == 0:  # Se o arquivo estiver vazio
            escritor.writerow(['ID', 'setor', 'nome', 'preco', 'data de validade', 'quantidade em estoque'])
        escritor.writerow([lista_produto['ID'], lista_produto['setor'], lista_produto['nome'], lista_produto['preco'], lista_produto['data de validade'], lista_produto['quantidade em estoque']])
    return

def editar_produto():
    with open('produtos.csv', 'r', encoding='utf8', newline='') as arquivo:
        leitor = csv.DictReader(arquivo)
        print('Lista de produtos cadastrados:\n')
        for linha in leitor:
            print(f"ID: {linha['ID']}   Produto: {linha['nome']}\n")
        resp = input('Digite o ID do produto que deseja alterar: ')
        
        # Resetando o cursor do arquivo para o início
        arquivo.seek(0)
        os.system('cls') or None
        for linha in leitor:
            if linha['ID'] == resp:
                break
        
        print('Informações do produto: \n')
        cont = 1
        for chave, valor in linha.items():
            if chave == 'ID':
                pass
            elif chave == 'data de validade':
                valor = eval(valor)
                valor_formartado = '/'.join(valor)
                print(f'{cont}: {chave} : {valor_formartado}')
                cont += 1
            else:
                print(f'{cont}: {chave} : {valor}')
                cont += 1
        
        resp_opcao = int(input('Digite o número da opção que deseja alterar: '))
        os.system('cls') or None
        # Resetando o cursor do arquivo para o início novamente
        arquivo.seek(0)
        next(leitor)  # Ignorando o cabeçalho
        
        # Localizando a linha específica no arquivo e armazenando-a
        for linha_atual in leitor:
            if linha_atual['ID'] == resp:
                linha_alterar = linha_atual
                break
        
        if resp_opcao == 3:  # Se for alterar o preço
            valor = "{:.2f}".format(round(float(input('Digite o valor a ser atribuído: '))))
        elif resp_opcao == 4:
            lista_data_validade = ['dia', 'mês', 'ano']
            for i in range(3):
                lista_data_validade[i] = input(f"Digite o {lista_data_validade[i]} da data de validade do produto: \n ")
                os.system('cls')
            valor = lista_data_validade
        elif resp_opcao == 5:  # Se for alterar a quantidade em estoque
            valor = int(input('Digite o valor a ser atribuído: '))
        else:
            valor = input('Digite o valor a ser atribuído: ')
        
        # Atualizando o valor na linha específica
        lista_chaves = list(linha_alterar.keys())
        chave_alterar = lista_chaves[resp_opcao]  
        linha_alterar[chave_alterar] = valor
        
        # Reescrevendo todas as linhas do arquivo CSV com a linha alterada
        linhas = []
        with open('produtos.csv', 'r', encoding='utf8', newline='') as arquivo:
            leitor = csv.DictReader(arquivo)
            for linha in leitor:
                if linha['ID'] == resp:
                    linhas.append(linha_alterar)
                else:
                    linhas.append(linha)
        
        with open('produtos.csv', 'w', encoding='utf8', newline='') as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=leitor.fieldnames)
            escritor.writeheader()
            escritor.writerows(linhas)
        
        input("Produto alterado com sucesso.")
        os.system('cls')
        return
    
def lista_produtos_setor():
    # Verifica se o arquivo "produtos.csv" existe
    if not os.path.exists('produtos.csv'):
        print("O arquivo 'produtos.csv' não foi encontrado.")
        return

    # Dicionário para armazenar os produtos por setor
    produtos_por_setor = {
        1: 'Higiene',
        2: 'Limpeza',
        3: 'Bebidas',
        4: 'Frios',
        5: 'Padaria',
        6: 'Açougue'
    }

    # Dicionário para armazenar os produtos lidos do arquivo
    produtos = {}

    # Lê o arquivo "produtos.csv" e organiza os produtos por setor
    with open('produtos.csv', 'r', newline='') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            setor = int(linha['setor'])
            nome_produto = linha['nome']
            if setor not in produtos:
                produtos[setor] = []
            produtos[setor].append(nome_produto)

    # Mostra a lista de produtos por setor
    print("Lista de produtos por setor:")
    for setor, nome_setor in produtos_por_setor.items():
        print(f"Setor: {nome_setor}")
        if setor in produtos:
            for produto in produtos[setor]:
                print(f"- {produto}")
        else:
            print("Nenhum produto encontrado para este setor.")
        print()
    input()
    os.system('cls') or None
    return  


# Função principal para exibir o painel do produto
def painel_produto():
    resp = input("""
        1: incluir novos produtos
        2: alterar produtos
        3: lista de produtos por setor
        4: Voltar
    """)
    os.system('cls')
    if resp == '1':
        return incluir_produto()
    elif resp == '2':
        return editar_produto()
    elif resp == '3':
        return lista_produtos_setor()
    else:
        return