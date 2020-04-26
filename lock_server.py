#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 2 - lock_server.py
"""

# Zona para fazer importação
import sock_utils
import sys, struct, pickle
import time
from lock_skel import Skel
import select as sel


# código do programa principal

if len(sys.argv) == 6:
    porta = (sys.argv[1])
    numeroRecursos = int(sys.argv[2])
    bloqueiosPermitidosPorRecurso = (sys.argv[3])
    bloqueiosPermitidosTotal = (sys.argv[4])
    tempoConcessao = (sys.argv[5])
    host = '127.0.0.1'
else:
    print('RUN: python3 lock_server.py <PORT> <NUMBER_OF_RESOURCES> <NUMBER_OF_LOCKS_ALLOWED_BY_RESOURCE> <NUMBER_OF_LOCKS_ALLOWED_IN_A_MOMENT> <CONCESSION TIME>')
    exit()

socket = sock_utils.create_tcp_server_socket(host, int(porta), 1)
locks = Skel(numeroRecursos, bloqueiosPermitidosPorRecurso, bloqueiosPermitidosTotal, tempoConcessao)

SocketList = [socket]
print ("\n<" + time.ctime() + "> " + 'Servidor Criado em %s:%s\n' % (host, porta))
print("                        Numero de Recursos: " + str(numeroRecursos))
print("          Bloqueios Permitidos por Recurso: " + str(bloqueiosPermitidosPorRecurso))
print("Numero Total de Bloqueios num dado Momento: " + str(bloqueiosPermitidosTotal))
print("           Tempo de Concessao dos Recursos: " + str(tempoConcessao))
print("\nÀ espera de clientes.\n")

##ciclo:
try:
    while True:
        R, W, X = sel.select(SocketList, [], [])
        for sckt in R:
            if sckt is socket:
                conn_sock, addr = socket.accept()
                addr, port = conn_sock.getpeername()
                print ("<" + time.ctime() + "> " + '   Nova Ligação:   %s:%d' % (addr, port))
                SocketList.append(conn_sock)
            else:
                locks.locks.clear_expired_locks()
                for recurso in locks.locks.recursosArray:
                    if locks.locks.recursosArray[recurso].stat() >= int(locks.locks.numMaxBloqueios):
                        locks.locks.recursosArray[recurso].disable()
                size_bytes2 = sckt.recv(4)
                if size_bytes2:
                    mensagem = sock_utils.receive_all(sckt, size_bytes2)
                    if mensagem:
                        print("\n-#-") 
                        print ("Recebi: ", mensagem)
                        resposta = locks.handleMessage(mensagem)
                        print ("Vou Enviar: ", resposta)
                        print("-#-\n")  
                        msg_bytes3 = pickle.dumps(resposta, -1)
                        size_bytes3 = struct.pack('!i',len(msg_bytes3))
                        sckt.sendall(size_bytes3)
                        sckt.sendall(msg_bytes3)
                        
                    print("Data Actual: " + time.ctime() + "\n")
                    print (locks.locks)
                    print ('----------#########----------\n')
                        
                else:
                    sckt.close()
                    SocketList.remove(sckt)
                    print ("<" + time.ctime() + "> " + 'Ligação Terminada: '  + str(addr) + ":" + str(port))    
    
    socket.close()

except KeyboardInterrupt:
    print ('\n<' + time.ctime() + '> Keyboard Interrupt')
    exit()
    
except Exception as e:
    if type(e) == ValueError:
        resposta = "INVALID ARGUMENT"

    else:
        print (e)
        resposta = "UNKNOWN ERROR"

finally:
    socket.close()