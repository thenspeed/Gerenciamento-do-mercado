# -*- Codado: utf-8 -*- 
# ----------------------------------------------------------------------------
# Criado By  : Bernardo Vieira Barros, Daniel Vieira Soares, Marcella Silva dos Santos Guimarães e Maria Gabriely Rodrigues Rissão
# Criação data: 10/04/2024 path de atualização 
# Versão = '1.0'
# ---------------------------------------------------------------------------

# """ Sistema de Gestão para um mercado de bairro """  # 
# ---------------------------------------------------------------------------

import os
import sys
import time
from produto import *
from cliente import *
from vendas import *

# ---------------------------------------------------------------------------



def flashy_print(text, color='\033[1;36m', blink=True):
    if blink:
        for _ in range(5):
            sys.stdout.write('\r' + color + text + '\033[0m')
            sys.stdout.flush()
            time.sleep(0.5)
            sys.stdout.write('\r' + ' ' * len(text))
            sys.stdout.flush()
            time.sleep(0.5)
    else:
        print(color + text + '\033[0m')


def loading_animation():
    bar_length = 20
    for i in range(bar_length + 1):
        sys.stdout.write('\r')
        sys.stdout.write("[%-20s] %d%%" % ('=' * i, 5 * i))
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\n')


def painel():
    os.system('cls')
    print('********.Sistema de Gestão do Mercado do Bairro.********\n')
    print('Escolha uma opção:\n')
    resp = input("""
        1: Painel produto
        2: Painel cadastro de cliente
        3: Painel de novas vendas
        4: Sair do aplicativo    
          """)
    os.system('cls')  # limpa a tela
    if resp == '1':
        painel_produto()
    elif resp == '2':
        painel_cliente()
    elif resp == '3':
        painel_venda()
    return resp


if __name__ == "__main__":
    flashy_print('Sistema de Gestão do Mercado do Bairro', color='\033[1;33m', blink=True)
    loading_animation()
    i = '0'
    while i != '4':
        i = painel()
