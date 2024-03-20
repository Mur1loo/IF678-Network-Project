import socket
import threading

class CertificationUnit:
    def __init__(self):
        self.UC_port = 50000
        self.UC_host = 'localhost'
        self.mensages = []

        #criação do socket da unidade certificadora
        self.UC_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.UC_socket.bind((self.UC_host, self.UC_port))
        self.UC_socket.listen()

    def receive_messages(self):
        """
        Accepts incoming PCs connections and receives messages from the PCs.

        :returns: None
        """
        client_socket, addr = self.UC_socket.accept()  # Accept incoming client connection
        while True:
            data = client_socket.recv(2048).decode()  # Receive data from client
            self.mensages.append(data)
            try:
                if not data:
                    break
                print("Mensagem recebida: " + data)  # Print received message
            except Exception as e:
                print(f"Erro {str(e)} ao receber mensagem")  # Print error message
                break
            finally:
                client_socket.close()  # Close socket

    def start(self):
        """
                Starts the Certification Unit to accept connections and creates a new thread for each PC.

                :returns: None
        """
        while True:
            client_socket, addr = self.UC_socket.accept()  # Accept new connection
            client_thread = threading.Thread(target=self.receive_messages, args=(client_socket, addr))
            client_thread.start()  # Start a new thread for the connected client