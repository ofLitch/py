import socket
import json
import pickle
import mysql.connector
from dao import SubscriberDAO
class UDPServer:
    def __init__(self, host, port):
        """
        Initialize the UDP Server with host and port.

        :param host: The IP address or hostname to bind the server to.
        :param port: The port number to bind the server to.
        """
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.host, self.port))
        dao = SubscriberDAO()
        self.dao = dao
        print(f"UDP Server initialized and listening on {self.host}:{self.port}")


    def listen(self, buffer_size=2048):
        """
        Start listening for incoming messages from clients.

        :param buffer_size: The maximum amount of data to be received at once (default is 2048 bytes).
        """
        try:
            print("Waiting for messages from clients...")
            while True:
                data, client_address = self.server_socket.recvfrom(buffer_size)

                # Desencriptar el mensaje
                decrypted_message = data.decode()

                # Parsear el mensaje JSON
                try:
                    json_data = json.loads(decrypted_message)
                    identifier = json_data.get("identifier")
                    name = json_data.get("name")
                    email = json_data.get("email")

                    # Insertar suscriptor y conexión en la base de datos
                    self.dao.insert_subscriber(identifier, name, email, client_address[0], client_address[1])

                    # Responder con ACK
                    response = {"status": "ACK", "message": "Registro exitoso"}
                except json.JSONDecodeError:
                    response = {"status": "NACK", "message": "Error de formato JSON"}

                # Enviar respuesta al cliente
                encrypted_response = json.dumps(response).encode()
                self.server_socket.sendto(encrypted_response, client_address)
                print(f"Response sent to {client_address}: {response}")

        except Exception as e:
            print(f"Error while receiving message: {e}")

    def close(self):
        """
        Close the UDP server socket.
        """
        self.server_socket.close()
        print("UDP Server socket closed.")


# Ejemplo de uso:
if __name__ == "__main__":
    server = UDPServer("0.0.0.0", 12000)
    server.listen()
    server.close()
