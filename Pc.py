from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread


class Pc:
    def __init__(self, pcnumber, uc):
        self.pcnumber = pcnumber
        self.client = socket(AF_INET, SOCK_DGRAM)
        self.servername = 'localhost'
        self.serverport = ''
        self.serverAddress = (self.servername, self.serverport)
        self.nex = None
        self.prev = None
        self.uc = uc
        self.key = None

        if not uc:
            self.serverport = 5000
            self.serverAddress = (self.servername, self.serverport)
            message = '.'
            self.client.sendto(message.encode(), self.serverAddress)
            data, saddress = self.client.recvfrom(2048)
            self.key = data.decode()
            self.client.close()

    def portchange(self, numberport):
        self.serverport = int(numberport)
        self.serverAddress = (self.servername, self.serverport)

    def handlerequest(self, mserversocket):
        message, clientaddress = self.client.recvfrom(2048)
        req = message.decode()
        if req == '.':
            rep = 'chave'
            mserversocket.sendto(rep.encode(), clientaddress)
        else:
            print(f'Requisicao recebida de {clientaddress}')
            print(f'A requisicao foi:{req}')
            rep = f'Oi, aqui quem fala é {self.pcnumber}!'
            mserversocket.sendto(rep.encode(), clientaddress)

    def starserver(self):
        self.client = socket(AF_INET, SOCK_DGRAM)
        self.client.bind((self.servername, self.serverport))
        print('The server is ready to receive')

        for i in range(2):
            Thread(target=self.handlerequest, args=(self.client,)).start()

    def startuc(self):
        self.client = socket(AF_INET, SOCK_DGRAM)
        self.client.bind((self.servername, self.serverport))
        for i in range(6):
            Thread(target=self.handlerequest, args=(self.client,)).start()

    def sendmessage(self, neighbor):
        if self.uc or neighbor == self.prev or neighbor == self.nex:

            self.client = socket(AF_INET, SOCK_DGRAM)
            while True:
                message = input('>>')
                if message == 'exit':
                    self.client.close()
                    break
                self.client.sendto(message.encode(), self.serverAddress)
                data, saddress = self.client.recvfrom(2048)
                reply = data.decode()
                print(f'Resposta recebida:{reply}')
        else:
            print('Conexão indisponivel')

    def showpcnumber(self):
        return self.pcnumber

    def setnext_prev(self, chose1, chose2):
        self.nex = chose1
        self.prev = chose2

    def showprev(self):
        return self.prev.pcnumber

    def showkey(self):
        return self.key
