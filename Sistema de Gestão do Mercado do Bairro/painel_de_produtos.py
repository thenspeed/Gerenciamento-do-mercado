import time
import os
import csv

while True:
     cont = 10
     with open('produtos.csv', 'r', encoding='utf8', newline='') as arquivo:
        leitor = csv.DictReader(arquivo)
        print('Lista de produtos cadastrados:\n')
        for linha in leitor:
            cont = cont - 1
            print(f"ID: {linha['ID']}   Produto: {linha['nome']}\n")
            if cont == 0: break
        
        time.sleep(3)
        os.system('cls')
        cont = 10
        aux = 10
        while cont == 0:
            for linha in leitor[aux]:
                cont = cont - 1
                print(f"ID: {linha['ID']}   Produto: {linha['nome']}\n")
                time.sleep(3)
                os.system('cls')
                if cont == 0: break
                    