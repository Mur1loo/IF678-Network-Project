from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import rsa


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
        self.otherkeys = []

        if not uc:
            self.serverport = 5000
            self.serverAddress = (self.servername, self.serverport)
            message = '.'
            self.client.sendto(message.encode(), self.serverAddress)
            data, saddress = self.client.recvfrom(2048)
            new_data = data.decode().split(',')
            a = int(new_data[0][11:])
            b = int(new_data[1])
            c = int(new_data[2])
            d = int(new_data[3])
            e = int(new_data[4][:72])

            self.key = rsa.PrivateKey(a, b, c, d, e)
            self.client.close()

    def portchange(self, numberport):
        self.serverport = int(numberport)
        self.serverAddress = (self.servername, self.serverport)

    def handlerequest(self, mserversocket):
        message, clientaddress = self.client.recvfrom(2048)
        req = message
        print(req)
        print(type(req))
        print(self.key)
        req = rsa.decrypt(message, self.key)
        req = req.decode("utf-8")

        print(f'Requisicao recebida de {clientaddress}')
        print(f'A requisicao foi:{req}')
        rep = f'Oi, aqui quem fala é {self.pcnumber}!'
        mserversocket.sendto(rep.encode(), clientaddress)

    def handlerequestuc(self, mserversocket):
        message, clientaddress = self.client.recvfrom(2048)
        req = message.decode()
        if req == '.':
            pubkey, privkey = rsa.newkeys(512)
            #print(pubkey)
            #print(str(privkey))
            self.otherkeys.append(pubkey)
            rep = str(privkey)
            mserversocket.sendto(rep.encode(), clientaddress)
        else:
            idx = int(req)
            rep = str(self.otherkeys[idx - 1])
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
        for i in range(10):
            Thread(target=self.handlerequestuc, args=(self.client,)).start()

    def askforkey(self, needkey):
        self.client = socket(AF_INET, SOCK_DGRAM)
        self.serverport = 5000
        self.serverAddress = (self.servername, self.serverport)
        message = f'{needkey}'
        self.client.sendto(message.encode(), self.serverAddress)
        data, saddress = self.client.recvfrom(2048)
        chave = data.decode()
        self.client.close()
        return chave

    def sendmessage(self, neighbor):
        if self.uc or neighbor == self.prev or neighbor == self.nex:
            porta = self.serverport
            chave = self.askforkey(neighbor.pcnumber).split(',')
            chave1 = int(chave[0][10:])
            chave2 = int(chave[1][:6])
            chave = rsa.PublicKey(chave1, chave2)
            print(chave)
            self.serverport = porta
            self.serverAddress = (self.servername, self.serverport)
            self.client = socket(AF_INET, SOCK_DGRAM)
            while True:
                message = input('>>')
                if message == 'exit':
                    self.client.close()
                    break
                data = message.encode()
                message = rsa.encrypt(data, chave)
                print(message)
                print(type(message))
                self.client.sendto(message, self.serverAddress)
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

    def showpubkeys(self):
        return self.otherkeys
