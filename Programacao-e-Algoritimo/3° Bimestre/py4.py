"""
    Autor: Ian Correa
    Data: 28/08/2026
    Descrição: Calcula a soma dos números pares de 1 até um número informado.
"""

numero = int(input("Digite um numero inteiro positivo: "))
contador = 1
soma = 0

if numero > 0:
    while contador <= numero:

        if contador % 2 == 0:
            soma = soma + contador

        contador += 1

    print("Soma dos pares:", soma)

else:
    print("Numero invalido.")