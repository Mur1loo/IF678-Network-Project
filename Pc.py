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
        """
        Change the server port and address based on the input port number.

        Args:
        numberport (int): The new port number to set for the server.
        """
        self.serverport = int(numberport)
        """
        Update the server address using the new port number.
        """
        self.serverAddress = (self.servername, self.serverport)

    def handle_request(self, mserversocket):
        """
        Handle the incoming request from the client.

        Args:
        self: the class instance
        mserversocket: the main server socket

        Returns:
        None
        """
        # Receive the message and client address
        message, clientaddress = self.client.recvfrom(2048)

        # Set the request to the received message
        req = message

        # Print the request and its type
        print(req)
        print(type(req))
        print(self.key)

        # Decrypt the message using the key and decode it to utf-8
        req = rsa.decrypt(message, self.key)
        req = req.decode("utf-8")

        # Print the client address and the received request
        print(f'Requisicao recebida de {clientaddress}')
        print(f'A requisicao foi:{req}')

        # Prepare and send the reply to the client
        rep = f'Oi, aqui quem fala é {self.pcnumber}!'
        mserversocket.sendto(rep.encode(), clientaddress)

    def handle_request_uc(self, mserversocket):
        """
        Handle requests from a client by sending public/private key pairs.

        Args:
        - self: the instance of the class
        - mserversocket: the socket to communicate with the client
        """
        # Receive message and client address
        message, clientaddress = self.client.recvfrom(2048)
        req = message.decode()

        if req == '.':
            pubkey, privkey = rsa.newkeys(512)
            # Uncomment if you want to print the public and private keys
            # print(pubkey)
            # print(str(privkey))
            self.otherkeys.append(pubkey)
            rep = str(privkey)
            mserversocket.sendto(rep.encode(), clientaddress)
        else:
            idx = int(req)
            rep = str(self.otherkeys[idx - 1])
            mserversocket.sendto(rep.encode(), clientaddress)

    def start_server(self):
        """
        Initialize the server and start listening for client requests.
        """
        self.client = socket(AF_INET, SOCK_DGRAM)
        self.client.bind((self.servername, self.serverport))
        print('The server is ready to receive')

        # Start two threads to handle client requests concurrently
        for i in range(2):
            Thread(target=self.handle_request, args=(self.client,)).start()

    def startuc(self):
        """
        Initialize a client socket and start handling requests in a separate thread.
        """
        # Create a client socket
        self.client = socket(AF_INET, SOCK_DGRAM)

        # Bind the client socket to the server name and port
        self.client.bind((self.servername, self.serverport))

        # Start handling requests in separate threads
        for i in range(10):
            Thread(target=self.handlerequestuc, args=(self.client,)).start()

    def ask_for_key(self, need_key):
        """
        Sends a request for a key to the server and returns the key received.

        Args:
            need_key (str): The key that is needed.

        Returns:
            str: The key received from the server.
        """
        # Create a UDP socket
        self.client = socket(AF_INET, SOCK_DGRAM)

        # Set the server port
        self.server_port = 5000

        # Set the server address
        self.server_address = (self.server_name, self.server_port)

        # Convert the key to a message string
        message = f'{need_key}'

        # Send the message to the server
        self.client.sendto(message.encode(), self.server_address)

        # Receive data and server address from the server
        data, server_address = self.client.recvfrom(2048)

        # Decode the received data to get the key
        key = data.decode()

        # Close the client socket
        self.client.close()

        return key

    def sendmessage(self, neighbor):
        """
        Sends encrypted messages to a neighbor using RSA encryption.

        Args:
        - neighbor: The neighbor to whom the message will be sent

        Returns:
        - None
        """
        # Check if the connection is available and the neighbor is valid
        if self.uc or neighbor == self.prev or neighbor == self.nex:
            # Store the server port for later use
            porta = self.serverport

            # Retrieve the public key of the neighbor
            chave = self.askforkey(neighbor.pcnumber).split(',')
            chave1 = int(chave[0][10:])
            chave2 = int(chave[1][:6])
            chave = rsa.PublicKey(chave1, chave2)
            print(chave)

            # Restore the original server port and address
            self.serverport = porta
            self.serverAddress = (self.servername, self.serverport)
            self.client = socket(AF_INET, SOCK_DGRAM)

            # Start sending messages
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
                print(f'Received response: {reply}')
        else:
            print('Connection unavailable')

    def show_pc_number(self):
        """
        Returns the pcnumber attribute of the object.

        Returns:
        str: The pcnumber attribute of the object.
        """
        return self.pcnumber

    def set_next_prev(self, choice1, choice2):
        """
        Set the next and previous choices for the current node.

        Args:
        choice1: The next choice for the current node
        choice2: The previous choice for the current node
        """
        self.next = choice1
        self.prev = choice2

    def showprev(self):
        return self.prev.pcnumber

    def showkey(self):
        return self.key

    def showpubkeys(self):
        return self.otherkeys