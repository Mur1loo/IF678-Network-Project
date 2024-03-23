from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread

class Pc:
    """
    This class represents a peer in a peer-to-peer network.
    Each peer has a unique identifier (pcnumber), a client socket for communication,
    and the capability to change ports, handle requests, start a server, send messages,
    and keep track of its neighbors in the network.
    """

    def __init__(self, pcnumber):
        """
        Initializes a new instance of the Pc class with a given pcnumber.
        Sets up the client socket and server address with default values.
        """
        self.pcnumber = pcnumber
        self.client = socket(AF_INET, SOCK_DGRAM)
        self.servername = 'localhost'
        self.serverport = ''
        self.serverAddress = (self.servername, self.serverport)
        self.nex = None  # Next peer in the network
        self.prev = None  # Previous peer in the network

    def portchange(self, numberport):
        """
        Changes the port number of the server address to the given numberport.
        """
        self.serverport = int(numberport)
        self.serverAddress = (self.servername, self.serverport)

    def handlerequest(self, mserversocket):
        """
        Handles a single incoming request on the given mserversocket.
        Receives a message and prints the request and response.
        """
        message, clientaddress = self.client.recvfrom(2048)
        req = message.decode()
        print(f'Requisicao recebida de {clientaddress}')
        print(f'A requisicao foi:{req}')
        rep = f'Oi, aqui quem fala é {self.pcnumber}!'
        mserversocket.sendto(rep.encode(), clientaddress)

    def starserver(self):
        """
        Starts the server by binding to the specified server address and listening for incoming requests.
        Spawns two threads to handle incoming requests concurrently.
        """
        self.client.bind((self.servername, self.serverport))
        print('The server is ready to receive')

        for i in range(2):
            Thread(target=self.handlerequest, args=(self.client,)).start()

    def sendmessage(self, neighbor):
        """
        Sends a message to the specified neighbor if it is either the next or previous peer.
        Continues to prompt for messages and sends them until 'exit' is input.
        """
        if neighbor == self.prev or neighbor == self.nex:
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
        """
        Returns the unique pcnumber identifier of this peer.
        """
        return self.pcnumber

    def setnext_prev(self, chose1, chose2):
        """
        Sets the next and previous neighbors in the network to the given chose1 and chose2.
        """
        self.nex = chose1
        self.prev = chose2

    def showprev(self):
        """
        Returns the pcnumber of the previous neighbor in the network.
        """
        return self.prev.pcnumber
