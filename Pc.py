from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread

class Pc:
    """PC class for handling client-server communication over UDP."""
    
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
        """
        Changes the server port of the PC.
        
        Args:
        numberport (int): The new port number.
        """
        self.serverport = int(numberport)
        self.serverAddress = (self.servername, self.serverport)

    def handlerequest(self, mserversocket):
        """
        Handles incoming requests on the server socket.
        
        Args:
        mserversocket (socket): The main server socket to handle requests on.
        """
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
        """Starts the server to receive and handle requests."""
        self.client = socket(AF_INET, SOCK_DGRAM)
        self.client.bind((self.servername, self.serverport))
        print('The server is ready to receive')

        # Start two threads to handle requests
        for i in range(2):
            Thread(target=self.handlerequest, args=(self.client,)).start()

    def startuc(self):
        """Starts the user client to send and receive messages."""
        self.client = socket(AF_INET, SOCK_DGRAM)
        self.client.bind((self.servername, self.serverport))
        
        # Start six threads to handle requests for user clients
        for i in range(6):
            Thread(target=self.handlerequest, args=(self.client,)).start()

    def sendmessage(self, neighbor):
        """
        Sends a message to a neighbor or handles messages if the PC is a user client.
        
        Args:
        neighbor (Pc): The neighbor PC to communicate with.
        """
        # Send message only if the PC is a user client or the neighbor is the previous or next PC
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
        """Returns the PC number."""
        return self.pcnumber

    def setnext_prev(self, chose1, chose2):
        """
        Sets the next and previous PCs.
        
        Args:
        chose1 (Pc): The next PC.
        chose2 (Pc): The previous PC.
        """
        self.nex = chose1
        self.prev = chose2

    def showprev(self):
        """Returns the previous PC number."""
        return self.prev.pcnumber

    def showkey(self):
        """Returns the key if there is one."""
        return self.key
