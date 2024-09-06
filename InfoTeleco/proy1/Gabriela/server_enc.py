import socket

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
                encrypted_message, client2_info = data.split(b'||')
                client2_ip, client2_port = client2_info.decode().split(':')
                client2_port = int(client2_port)

                print(f"Received message from {client_address}, forwarding to {client2_ip}:{client2_port}")

                # Reenviar el mensaje cifrado al cliente2
                self.server_socket.sendto(encrypted_message, (client2_ip, client2_port))
                print(f"Message forwarded to {client2_ip}:{client2_port}")
                

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
