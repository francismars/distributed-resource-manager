# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 2 - lock_stub.py
"""

from net_client import server

class Stub:
    def __init__(self, host, port, client_id):
        self.conn_sock = None
        self.host = host
        self.port = port
        self.client_id = client_id

    def connect(self):
        # código para estabelecer uma ligação,
        # i.e., tornando self.conn_sock válida
        self.conn_sock = server(self.host,self.port)
        self.conn_sock.connect()

    def disconnect(self):
        # Fecha a ligação conn_sock
        self.conn_sock.close()
        
    def sendAndPrint(self, lista_enviada):
        if len(lista_enviada) != 0:
            print("\n-#-") 
            print ("Vou Enviar: " , lista_enviada)
            resposta = self.conn_sock.send_receive(lista_enviada)
            print ("Recebi: " , resposta)
            print("-#-\n")
        
    def lock(self, numRecurso):
        lista_enviada = []
        lista_enviada.append(10)
        lista_enviada.append(int(self.client_id))
        lista_enviada.append(int(numRecurso))
        self.sendAndPrint(lista_enviada)
        
    def release(self, numRecurso):
        lista_enviada = []
        lista_enviada.append(20)
        lista_enviada.append(int(self.client_id))
        lista_enviada.append(int(numRecurso))
        self.sendAndPrint(lista_enviada)  
    
    def test(self, numRecurso):
        lista_enviada = []
        lista_enviada.append(30)
        lista_enviada.append(int(numRecurso))
        self.sendAndPrint(lista_enviada)
            
    def stats(self, numRecurso):
        lista_enviada = []
        lista_enviada.append(40)
        lista_enviada.append(int(numRecurso))
        self.sendAndPrint(lista_enviada)
            
    def statsY(self):
        lista_enviada = []
        lista_enviada.append(50)
        self.sendAndPrint(lista_enviada)
            
    def statsN(self):
        lista_enviada = []
        lista_enviada.append(60)
        self.sendAndPrint(lista_enviada)