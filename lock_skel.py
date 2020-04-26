# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 2 - lock_skel.py
"""


import lock_pool

class Skel:
    def __init__(self, N, K, Y, T):
        self.locks = lock_pool.lock_pool(N, K, Y, T)

        
    def handleMessage(self, mensagem):
        resposta= []
        
        if mensagem[0] == 10: #LOCK
            try:
                resposta.append(11)
                client_id = mensagem[1]
                nr_resource = mensagem[2]
                if nr_resource > self.locks.numRecursos or nr_resource < 1:
                    resposta.append(None)
                else:
                    totalBloqueados = 0
                    permitirBloqueios = True
                    for recurso in self.locks.recursosArray:
                        if self.locks.recursosArray[recurso].test() == "LOCKED":
                            totalBloqueados += 1
                    if totalBloqueados >= int(self.locks.numMaxBloqueios):
                        permitirBloqueios = False
                
                    if permitirBloqueios == False:
                        resposta.append(False)
                    elif permitirBloqueios == True:
                        answer = self.locks.lock(nr_resource, client_id, self.locks.tempoMaxConcessao)
                    
                        if answer == True:
                            resposta.append(True)
                        elif answer == False:
                            resposta.append(False)
                            
            except:
                resposta = "except: UNKNOWN COMMAND"
	    
        elif mensagem[0] == 20: #RELEASE
            try:
                resposta.append(21)
                client_id = mensagem[1]
                nr_resource = mensagem[2]
                if nr_resource > self.locks.numRecursos or nr_resource < 1:
                    resposta.append(None)
                else:
                    answer = self.locks.release(nr_resource, client_id)
                    if answer == True:
                        resposta.append(True)
                    elif answer == False:
                        resposta.append(False)
            except:
                resposta = "RELEASE UNKNOWN COMMAND"
	    
        elif mensagem[0] == 30: #TEST
            try:
                resposta.append(31)
                nr_resource = mensagem[1]
                if len(self.locks.recursosArray) >= nr_resource > 0:
                    testeRecurso = self.locks.recursosArray[nr_resource-1].test()
                    if testeRecurso == "LOCKED":
                        resposta.append(False)
                    if testeRecurso == "UNLOCKED":
                        resposta.append(True)
                    if testeRecurso == "DISABLED":
                        resposta.append('disable')
                else:
                    resposta.append(None)
            except:
                resposta = 'TEST UNKNOWN COMMAND'
    	
        elif mensagem[0] == 40: #STATS
            try:
                resposta.append(41)
                nr_resource = mensagem[1]
                if len(self.locks.recursosArray) >= nr_resource > 0:
                    resposta.append(self.locks.stat(nr_resource))
                else:
                    resposta.append(None)
            except:
                resposta = "UNKNOWN COMMAND"
	    
        elif mensagem[0] == 50: #STATS-Y
            try:
                resposta.append(51)
                resposta.append(self.locks.stat_y())
            except:
                resposta = "UNKNOWN COMMAND"
	    
        elif mensagem[0] == 60: #STATS-N
            try:
                resposta.append(61)
                resposta.append(self.locks.stat_n())
            except:
                resposta = "UNKNOWN COMMAND"

        else:
            resposta = "UNKNOWN COMMAND"

        return resposta