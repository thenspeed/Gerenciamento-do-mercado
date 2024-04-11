import os
from produto import *
from cliente import *
from vendas import *


def painel():
    resp = input("""
        1: Painel produto
        2: Painel cadastro de cliente
        3: Painel de novas vendas
        4: Sair do aplicativo    
          """)
    os.system('cls')
    if resp == '1':
        painel_produto()
    elif resp == '2':
        painel_cliente()
    elif resp == '3':
        painel_venda()
    return resp

    




if __name__ == "__main__":
    i = '0'
    while i != '4':
        i = painel()
