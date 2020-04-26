#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 2 - lock_client.py
"""

from lock_stub import Stub
import sys

# Programa principal

if len(sys.argv) == 4:
    host = sys.argv[1]
    port = int(sys.argv[2])
    client_id= sys.argv[3]
else:
    print('RUN: python3 lock_client.py <HOST> <PORT> <CLIENT_ID>')
    exit()
    
cliente = Stub(host,port,client_id)
cliente.connect()

print ("> For Assistance type HELP.\n")

while True:
    try:
        comando = input("Comando > ")
        if len(comando) != 0:
            parametros = comando.split()
            mensagem = parametros[0].upper()
            if mensagem == "EXIT":
                cliente.disconnect()
                exit()
            elif mensagem == "HELP":
                print("Lista de Comandos:\n")
                print("Mensagem enviada             : Resposta do servidor")
                print("LOCK <numero do recurso>     : [11, True] ou [11, False] ou [11, None]")
                print("RELEASE <numero do recurso>  : [21, True] ou [21, False] ou [21, None]")
                print("TEST <numero do recurso>     : [31, True] ou [31, False] ou [31, disable] ou [31, None]")
                print("STATS <numero do recurso>    : [41, <nº de bloqueios do recurso em K>] ou [41, None]")
                print("STATS-Y                      : [51, <nº de recursos bloqueados em Y]")
                print("STATS-N                      : [61, <nº de recursos disponíveis]")
            elif mensagem == "LOCK":
                if len(parametros) != 2:
                    print ("> Not Enough Arguments. For Assistance type HELP.")
                else:
                    cliente.lock(parametros[1])
            elif mensagem == "RELEASE":
                if len(parametros) != 2:
                    print ("> Not Enough Arguments. For Assistance type HELP.")
                else:
                    cliente.release(parametros[1])
            elif mensagem == "TEST":
                if len(parametros) != 2:
                    print ("> Not Enough Arguments. For Assistance type HELP.")
                else:
                    cliente.test(parametros[1])
            elif mensagem == "STATS":
                if len(parametros) != 2:
                    print ("> Not Enough Arguments. For Assistance type HELP.")
                else:
                    cliente.stats(parametros[1])
            elif mensagem == "STATS-Y":
                cliente.statsY()
            elif mensagem == "STATS-N":
                cliente.statsN()
            else:
                print ('> For Assistance type HELP.')
        else:
            print ('> For Assistance type HELP.')

    except KeyboardInterrupt:
        print ('\nKeyboard Interrupt')
        cliente.disconnect()
        exit()