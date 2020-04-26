# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 2 - net_client.py
"""

# zona para fazer importação

from sock_utils import *
import time

# definição da classe server 

class server:
    def __init__(self, address, port):
        self.host = address
        self.port = port
        
    def connect(self):
        self.socket = create_tcp_client_socket(self.host, self.port)
        addr, port = self.socket.getsockname() #assumimos que sock esta conectado
        print ('\n<' + time.ctime() + '> Ligado pelo endereço local %s:%d\n' % (addr, port))
        

    def send_receive(self, data):
        msg_bytes = pickle.dumps(data, -1)
        size_bytes = struct.pack('!i',len(msg_bytes))
        self.socket.sendall(size_bytes)
        self.socket.sendall(msg_bytes)
        size_bytes2 = self.socket.recv(4)
        return receive_all(self.socket, size_bytes2)
    
    def close(self):
        self.socket.close()
        print ('<' + time.ctime() + '> Ligação Terminada')