import socket
import threading
import pickle
import json


class UDPClient:
    def __init__(self, server_ip, server_port, client2_ip, client2_port, local_ip, local_port):
        """
        Initialize the UDP Client with server IP and port.

        :param server_ip: The IP address of the server.
        :param server_port: The port number of the server.
        """
        self.server_ip = server_ip
        self.server_port = server_port
        self.client2_ip = client2_ip
        self.client2_port = client2_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.bind((local_ip, local_port))
        self.listening = False
        print(f"UDP Client initialized for server at {self.server_ip}:{self.server_port}")

    def send_register_request(self, identifier, name, email):
        """
        Send a registration request (in JSON) to the server.

        :param identifier: The unique identifier of the subscriber.
        :param name: Name of the subscriber.
        :param email: Email of the subscriber.
        """
        try:
            # Crear el registro en formato JSON
            register_data = {
                "identifier": identifier,
                "name": name,
                "email": email
            }
            json_data = json.dumps(register_data)

            # Encriptar el mensaje
            enc_message = json_data.encode()

            # Enviar el mensaje al servidor
            self.client_socket.sendto(enc_message, (self.server_ip, self.server_port))
            print(f"Registro enviado al servidor {self.server_ip}:{self.server_port}")

        except Exception as e:
            print(f"Failed to send registration request: {e}")

    def _listen_for_messages(self, buffer_size=1024):
        """
        Private method to listen for messages from the server. Intended to run in a separate thread.

        :param buffer_size: The maximum amount of data to be received at once (default is 1024 bytes).
        """
        try:
            print("Started listening for messages from the server...")
            while self.listening:
                data, client_address = self.client_socket.recvfrom(buffer_size)
                dec_message = data.decode()

                # Decodificar el mensaje JSON
                response_data = json.loads(dec_message)
                print(f"Received response from {client_address}: {response_data}")

        except Exception as e:
            print(f"Error receiving message: {e}")

    def start_listening(self):
        """
        Start listening for server messages on a separate thread.
        """
        self.listening = True
        self.listen_thread = threading.Thread(target=self._listen_for_messages)
        self.listen_thread.daemon = True  # Daemon thread will exit when the main program exits
        self.listen_thread.start()

    def stop_listening(self):
        """
        Stop listening for server messages.
        """
        self.listening = False
        if self.listen_thread.is_alive():
            self.listen_thread.join()  # Wait for the listening thread to finish
        print("Stopped listening for server messages.")

    def close(self):
        """
        Close the UDP client socket and stop listening.
        """
        self.stop_listening()
        self.client_socket.close()
        print("UDP Client socket closed.")


# Ejemplo de uso:
if __name__ == "__main__":
    client = UDPClient("127.0.0.1", 12000, "127.0.0.1", 6000, "127.0.0.1", 5000)

    # Iniciar escucha de mensajes en un hilo separado
    client.start_listening()

    # Enviar solicitudes de registro
    try:
        while True:
            identifier = input("Enter identifier: ")
            name = input("Enter name: ")
            email = input("Enter email: ")

            if identifier.lower() == 'exit':
                break

            client.send_register_request(identifier, name, email)
    except KeyboardInterrupt:
        print("\nClient interrupted.")

    # Cerrar el cliente
    client.close()
