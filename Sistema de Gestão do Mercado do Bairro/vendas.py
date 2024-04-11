import os
import csv
from cliente import incluir_cliente
import subprocess
import math
from datetime import datetime, timedelta

lista_venda = {'ID': 0, 'cpf': 0, 'data da compra': 0, 'valor total da compra': 0, 'quantidade de produtos': 0}
lista_Itens_compra = {'ID_venda': 0, 'cpf': 0, 'ID_produto': 0, 'quantidade': 0, 'preco unitario': 0, 'preco total': 0}

def gerador_Id_venda():
    contador = 0
    try:
        with open('vendas.csv', 'r', encoding='utf8', newline='') as arquivo:
            leitor = csv.reader(arquivo)
            for x in leitor:
                contador += 1
        return contador
    except:
        with open('vendas.csv', 'a', encoding='utf8', newline='') as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(['ID', 'cpf', 'data da compra', 'valor total da compra', 'quantidade de produtos'])
        return contador

def validar_cpf(cpf):
    try:
        with open('clientes.csv', 'r', newline='') as arquivo:
            leitor = csv.DictReader(arquivo)
            linhas = list(leitor)

        for linha in linhas:
            if linha['CPF'] == cpf:
                return
            else:
                print('O CPF digitado ainda não consta em nossa base de dados. Será necessário realizar \num cadastro para continuar com a venda')
                input()
                os.system('cls') or None
                incluir_cliente()
                return
    except:
        incluir_cliente()

def painel_nova_venda():
    id = gerador_Id_venda()
    lista_venda['ID'] = id
    lista_venda['quantidade de produtos'] = 0
    cpf = input("Digite o CPF do cliente: ")
    validar_cpf(cpf)
    os.system('cls') or None
    lista_venda['cpf'] = cpf
    resp = '0'

    try:
        subprocess.Popen(["start", "cmd", "/k", "python", "painel_de_produtos.py"], shell=True)
    except:
        subprocess.Popen(["gnome-terminal", "-e", "python3", "painel_de_produtos.py"])

    valor_total_da_compra = 0.0
    while resp != 'ok':
        lista_Itens_compra['ID_venda'] = id
        lista_Itens_compra['cpf'] = cpf
        id_produto = int(input('Digite o ID do produto que será comprado: \n'))
        lista_Itens_compra['ID_produto'] = id_produto
        os.system('cls') or None
        quantidade = int(input('Digite a quantidade desse produto que será comprada \n'))
        lista_Itens_compra['quantidade'] = quantidade
        os.system('cls') or None

        preco_unitario = None
        with open('produtos.csv', 'r', encoding='utf8', newline='') as arquivo:
            leitor = csv.DictReader(arquivo)
            produtos = list(leitor)
            for linha in produtos:
                if linha['ID'] == str(id_produto):
                    preco_unitario = "{:.2f}".format(round(float(linha['preco']), 2))
                    if int(linha['quantidade em estoque']) < quantidade:
                        input("Não há quantidade disponível do produto")
                        break
                    else:
                        lista_Itens_compra['preco unitario'] = preco_unitario
                        preco_total = float(preco_unitario) * quantidade
                        lista_Itens_compra['preco total'] = "{:.2f}".format(round(preco_total, 2))
                        linha['quantidade em estoque'] = int(linha['quantidade em estoque']) - quantidade

                        # Atualizando o arquivo produtos.csv
                        with open('produtos.csv', 'w', encoding='utf8', newline='') as arquivo_atualizado:
                            escritor = csv.DictWriter(arquivo_atualizado, fieldnames=leitor.fieldnames)
                            escritor.writeheader()
                            for produto in produtos:
                                if produto['ID'] == str(id_produto):
                                    escritor.writerow(linha)
                                else:
                                    escritor.writerow(produto)
                        break

        
        if lista_Itens_compra['preco unitario'] is None:
            resp = resp
        else: 
            lista_venda['quantidade de produtos'] += 1
            cabecalho = ['ID_venda', 'cpf', 'ID_produto', 'quantidade', 'preco unitario', 'preco total']
            with open('ItensCompra.csv', 'a', encoding='utf8', newline='') as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=cabecalho)
                escritor.writerow({
                                    'ID_venda': lista_Itens_compra['ID_venda'],
                                    'cpf': lista_Itens_compra['cpf'],
                                    'ID_produto': lista_Itens_compra['ID_produto'],
                                    'quantidade': lista_Itens_compra['quantidade'],
                                    'preco unitario': lista_Itens_compra['preco unitario'],
                                    'preco total': lista_Itens_compra['preco total']
                                    })

            valor_total_da_compra =+ preco_total
            resp = input('Aperte qualquer tecla para acrescentar a compra de mais produtos ou\ndigite "ok" para finalizar a lista de itens: \n')
            os.system('cls') or None
    if lista_venda['quantidade de produtos'] == 0:
        return
    else:
        data_atual = datetime.now()
        data_formatada = [data_atual.strftime('%d'), data_atual.strftime('%m'), data_atual.strftime('%Y')]
        lista_venda['data da compra'] = data_formatada
        lista_venda['valor total da compra'] = "{:.2f}".format(valor_total_da_compra)
        os.system('cls') or None

        for chave, valor in lista_venda.items():
            if chave != 'data da compra':
                print(f'{chave}: {valor}')
            else:
                valor_formartado = '/'.join(valor)
                print(f'{chave}: {valor_formartado}')
        input('')
        os.system('cls') or None
        with open('vendas.csv', 'a') as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow([lista_venda['ID'], lista_venda['cpf'], lista_venda['data da compra'], lista_venda['valor total da compra'], lista_venda['quantidade de produtos']])
        pontos_clientes(lista_venda['cpf'], lista_venda['valor total da compra'])
        return

def pontos_clientes(cpf_comprador, pontos):
    linhas_atualizadas = []

    # Lê o arquivo CSV e busca a linha correspondente ao CPF do cliente
    with open('clientes.csv', 'r', newline='') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            if linha['CPF'] == cpf_comprador:
                # Converte a quantidade de pontos para float e soma com os pontos existentes
                pontos_totais = float(linha['pontos']) + float(pontos)
                # Arredonda para baixo a quantidade total de pontos
                pontos_totais = math.floor(pontos_totais)
                linha['pontos'] = pontos_totais  # Atualiza a quantidade de pontos na linha
            linhas_atualizadas.append(linha)  # Adiciona a linha (alterada ou não) na lista

    # Escreve as linhas atualizadas no arquivo CSV
    with open('clientes.csv', 'w', newline='') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=leitor.fieldnames)
        escritor.writeheader()
        escritor.writerows(linhas_atualizadas)
        return



def mostrar_produtos_mais_vendidos():
    # Passo 1: Consultar os CPFs que realizaram compras nos últimos 3 dias
    cpf_compras_recentes = set()
    data_limite = datetime.now() - timedelta(days=3)

    with open('vendas.csv', 'r', newline='') as arquivo_vendas:
        leitor_vendas = csv.DictReader(arquivo_vendas)
        for linha in leitor_vendas:
            data_compra = datetime.strptime(linha['data da compra'].strip("[]").replace("'", ""), '%d, %m, %Y')
            if data_compra >= data_limite:
                cpf_compras_recentes.add(linha['cpf'])

    # Passo 2: Consultar os IDs dos produtos mais comprados nos últimos 3 dias
    produtos_mais_comprados = {}
    with open('ItensCompra.csv', 'r', newline='') as arquivo_itens_compra:
        leitor_itens_compra = csv.DictReader(arquivo_itens_compra)
        for linha in leitor_itens_compra:
            if linha['cpf'] in cpf_compras_recentes:
                id_produto = int(linha['ID_produto'])
                quantidade = int(linha['quantidade'])
                if id_produto in produtos_mais_comprados:
                    produtos_mais_comprados[id_produto] += quantidade
                else:
                    produtos_mais_comprados[id_produto] = quantidade

    # Passo 3: Consultar as informações dos produtos nos arquivos CSV e mostrar ao usuário
    with open('produtos.csv', 'r', newline='') as arquivo_produtos:
        leitor_produtos = csv.DictReader(arquivo_produtos)
        produtos_info = {int(produto['ID']): produto for produto in leitor_produtos}

    # Passo 4: Mostrar os nomes dos produtos mais comprados ao usuário
    print("Os produtos mais comprados nos últimos 3 dias são:")
    for id_produto, quantidade in sorted(produtos_mais_comprados.items(), key=lambda x: x[1], reverse=True)[:5]:
        produto_info = produtos_info.get(id_produto)
        if produto_info:
            print(f"{produto_info['nome']} - Quantidade vendida: {quantidade}")
        
    input()
    os.system('cls')
    return





# Função principal para exibir o painel do produto
def painel_venda():
    resp = input("""
        1: realizar uma venda
        2: mostrar os 5 mais vendidos nos últimos 3 dias
        3: Voltar
    """)
    os.system('cls')
    if resp == '1':
        return painel_nova_venda()
    elif resp == '2':
        return mostrar_produtos_mais_vendidos()
    else:
        return
