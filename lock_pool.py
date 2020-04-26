# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 2 - lock_pool.py
"""


import time

###############################################################################

class resource_lock:
    def __init__(self):
        """
        Define e inicializa as características de um LOCK num recurso.
        """
        self.estado = "UNLOCKED"
        self.blockedCounter = 0
        self.clienteComConcessao = 0
        self.tempoDeConcessao = 0
        self.timeOfLock = 0

    def lock(self, client_id, time_limit):
        """
        Bloqueia o recurso se este não estiver bloqueado ou inativo, ou mantém o bloqueio
        se o recurso estiver bloqueado pelo cliente client_id. Neste caso renova
        o bloqueio do recurso até time_limit.
        Retorna True se bloqueou o recurso ou False caso contrário.
        """
        if self.estado == "UNLOCKED":
            self.blockedCounter += 1
            self.clienteComConcessao = client_id
            self.tempoDeConcessao = time_limit
            self.timeOfLock = time.time()
            self.estado = "LOCKED"
            return True
        if self.estado == "LOCKED":
            if client_id == self.clienteComConcessao:
                self.blockedCounter += 1
                self.tempoDeConcessao = time_limit
                self.timeOfLock = time.time()
                return True
        return False
            
    def urelease(self):
        """
        Liberta o recurso incondicionalmente, alterando os valores associados
        ao bloqueio.
        """
        self.estado = "UNLOCKED"
        self.clienteComConcessao = 0
        self.tempoDeConcessao = 0
        self.timeOfLock = 0

    def release(self, client_id):
        """
        Liberta o recurso se este foi bloqueado pelo cliente client_id,
        retornando True nesse caso. Caso contrário retorna False.
        """
        if self.estado == "LOCKED":
            if client_id == self.clienteComConcessao:
                self.estado = "UNLOCKED"
                self.clienteComConcessao = 0
                self.tempoDeConcessao = 0
                self.timeOfLock = 0
                return True
        return False

    def test(self):
        """
        Retorna o estado de bloqueio do recurso ou inativo, caso o recurso se 
        encontre inativo.
        """
        return self.estado # Remover esta linha e fazer implementação da função
    
    def stat(self):
        """
        Retorna o número de vezes que este recurso já foi bloqueado em k.
        """
        return self.blockedCounter # Remover esta linha e fazer implementação da função

    def disable(self):
        """
        Coloca o recurso inativo/indisponível incondicionalmente, alterando os 
        valores associados à sua disponibilidade.
        """
        self.clienteComConcessao = 0
        self.tempoDeConcessao = 0
        self.timeOfLock = 0
        self.estado = "DISABLED"

        
###############################################################################

class lock_pool:
    def __init__(self, N, K, Y, T):
        """
        Define um array com um conjunto de locks para N recursos. Os locks podem
        ser manipulados pelos métodos desta classe.
        Define K, o número máximo de bloqueios permitidos para cada recurso. Ao 
        atingir K, o recurso fica indisponível/inativo.
        Define Y, o número máximo permitido de recursos bloqueados num dado 
        momento. Ao atingir Y, não é possível realizar mais bloqueios até que um 
        recurso seja libertado.
		Define T, o tempo máximo de concessão de bloqueio.
        """
        self.recursosArray = {}
        self.numRecursos = N
        self.numMaxBloqueios = K
        self.numMaxRecursosBloqueados = Y
        self.tempoMaxConcessao = T
        
        for recurso in range(self.numRecursos):
            self.recursosArray[recurso] = resource_lock()
        
    def clear_expired_locks(self):
        """
        Verifica se os recursos que estão bloqueados ainda estão dentro do tempo
        de concessão do bloqueio. Liberta os recursos caso o seu tempo de
        concessão tenha expirado.
        """
        for recurso in self.recursosArray:
            if self.recursosArray[recurso].test() == "LOCKED":
                if int(self.tempoMaxConcessao) < (time.time() - self.recursosArray[recurso].timeOfLock):
                    self.recursosArray[recurso].urelease()
            

    def lock(self, resource_id, client_id, time_limit):
        """
        Tenta bloquear o recurso resource_id pelo cliente client_id, até ao
        instante time_limit.
        O bloqueio do recurso só é possível se o recurso estiver ativo, não 
        bloqueado ou bloqueado para o próprio requerente, e Y ainda não foi 
        excedido. É aconselhável implementar um método __try_lock__ para
        verificar estas condições.
        Retorna True em caso de sucesso e False caso contrário.
        """
        numActualRecursosBloqueados = 0
        for recurso in self.recursosArray:
            if self.recursosArray[recurso].test() == "LOCKED":
                numActualRecursosBloqueados += 1
        
        if int(numActualRecursosBloqueados) >= int(self.numMaxRecursosBloqueados):
            return False
        if int(numActualRecursosBloqueados) <= int(self.numMaxRecursosBloqueados):
            if self.recursosArray[resource_id-1].test() == "UNLOCKED":
                self.recursosArray[resource_id-1].lock(client_id, time_limit)
                return True
            
            if self.recursosArray[resource_id-1].test() == "LOCKED":
                if self.recursosArray[resource_id-1].clienteComConcessao == client_id:
                    self.recursosArray[resource_id-1].lock(client_id, time_limit)
                    return True
        return False

    def release(self, resource_id, client_id):
        """
        Liberta o bloqueio sobre o recurso resource_id pelo cliente client_id.
        True em caso de sucesso e False caso contrário.
        """
        return self.recursosArray[resource_id-1].release(client_id)

    def test(self,resource_id):
        """
        Retorna True se o recurso resource_id estiver desbloqueado e False caso 
        esteja bloqueado ou inativo.
        """
        if self.recursosArray[resource_id-1].test() == "UNLOCKED":
            return True
        else:
            return False

    def stat(self,resource_id):
        """
        Retorna o número de vezes que o recurso resource_id já foi bloqueado, dos 
        K bloqueios permitidos.
        """
        return self.recursosArray[resource_id-1].blockedCounter

    def stat_y(self):
        """
        Retorna o número de recursos bloqueados num dado momento do Y permitidos.
        """
        numActualRecursosBloqueados = 0
        for recurso in self.recursosArray:
            if self.recursosArray[recurso].test() == "LOCKED":
                numActualRecursosBloqueados += 1
        return numActualRecursosBloqueados

    def stat_n(self):
        """
        Retorna o número de recursos disponíneis em N.
        """
        numActualRecursosDisponiveis = 0
        for recurso in self.recursosArray:
            if self.recursosArray[recurso].test() == "UNLOCKED":
                numActualRecursosDisponiveis += 1
        return numActualRecursosDisponiveis
		
    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print.
        """
        output = ""
        for recurso in range(self.numRecursos):
            if self.recursosArray[recurso].test() == "LOCKED":
                output += "Recurso " + str(recurso+1) + " bloqueado pelo cliente " + str(self.recursosArray[recurso].clienteComConcessao) + " até " + time.ctime(self.recursosArray[recurso].timeOfLock + float(self.recursosArray[recurso].tempoDeConcessao)) + "\n"
            if self.recursosArray[recurso].test() == "UNLOCKED":
                output += "Recurso " + str(recurso+1) + " desbloqueado\n"
            if self.recursosArray[recurso].test() == "DISABLED":
                output += "Recurso " + str(recurso+1) + " inativo\n"
        return output

###############################################################################