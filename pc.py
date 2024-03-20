from CertificationUnit import CertificationUnit
import threading
import socket


class PC:

    def __init__(self):
        self._port = int(input("digite o número da porta: "))
        self._pc_number = int(input("digite o número do pc: "))
        self._neighbors = input("digite os vizinhos separados por espaços: ")
        self._neighbors = [int(x) for x in self._neighbors.split()]

        #socket's setup
        self.pc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pc_socket.bind(('localhost', self._port))

    @property
    def port(self) -> int:
        return self._port

    @property
    def pc_number(self) -> int:
        return self._pc_number

    def accept_connections(self):
        """
        Accept incoming connections and handle each client connection in a new thread.

        Returns:
        None
        """
        self.pc_socket.listen()
        while True:
            client_socket, addr = self.pc_socket.accept()
            threading.Thread(target=self.handleClient, args=(client_socket, addr))

    def start_listening(self):
        """
        Start listening for incoming connections, and handle each client connection in a new thread.

        Returns:
        None
        """
        print(f"PC {self.pc_number} listening on port {self.port}")
        threading.Thread(target=self.accept_connections).start()

    def handleClient(self, client_socket, addr):
        """
        Handle the client connection.

        Args:
        client_socket: the socket for the client connection
        addr: the address of the client

        Returns:
        None
        """
        while True:
            try:
                data = client_socket.recv(2048).decode()  # Receive data from the client
                print("Mensagem recebida: " + data)  # Print the received message
                if not data:  # Check if data is empty
                    break
            except Exception as e:
                print(f"Erro {str(e)} ao receber mensagem")  # Print error message
                break

    def send_messages_to_neighbors(self, message):
        """
        Send a message to a neighbor.

        Args:
        message (str): The message to be sent.
        destination (Neighbor): The destination neighbor to send the message to.

        Returns:
        bool: True if the message was sent successfully, False otherwise.
        """
        destination = input("digite o número do pc de destino: ")
        if int(destination) not in self._neighbors:
            print("Destino inválido")
            return False

        destination_port = int('5000' + str(destination))

        try:
            # Cria um novo socket para este vizinho
            neighbor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            neighbor_socket.connect(('localhost', destination_port))
            neighbor_socket.send(message.encode())
        except Exception as e:
            print(f"Erro ao conectar ao vizinho {destination}: {str(e)}")
            return False
        finally:
            # Fecha o socket após o uso
            neighbor_socket.close()

        return True


    def send_message_to_uc(self, message):
        """
        Send a message to the Certification Unit.

        Args:
        message (str): The message to be sent.

        Returns:
        bool: True if the message was sent successfully, False otherwise.
        """
        # Connect to the Certification Unit
        self.pc_socket.connect(('localhost', CertificationUnit.UC_port))

        # Send the message to the Certification Unit
        self.pc_socket.send(message.encode())
        return True