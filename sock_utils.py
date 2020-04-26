"""
Aplicações distribuídas - Projeto 2 - sock_utils.py
"""

# zona para fazer importação

import socket as s
import pickle, struct

# definição das funcoes

def create_tcp_server_socket(address, port, queue_size):

    socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR,1)
    socket.bind((address, port))
    socket.listen(queue_size)
    return socket
    

def create_tcp_client_socket(address, port):

    socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    socket.connect((address, port))
    return socket


def receive_all(socketMSG, length):
    
    size = struct.unpack('!i',length)[0]
    msg_bytes = socketMSG.recv(size)
    msg = pickle.loads(msg_bytes)
    return msg