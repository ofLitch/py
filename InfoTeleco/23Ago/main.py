import json
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

    def listen(self, buffer_size=1024):
        """
        Start listening for incoming messages from clients.

        :param buffer_size: The maximum amount of data to be received at once (default is 1024 bytes).
        :return: The message and the client's address.
        """
        try:
            print("Waiting for messages from clients...")
            while True:
                
                data, client_address = self.server_socket.recvfrom(buffer_size)
                message = data.decode('utf-8')
                print(f"Received message from {client_address}: {message}")

                # Optional: Reply to the client
                response_message = f"Server received your message: {message}"
                self.server_socket.sendto(response_message.encode('utf-8'), client_address)
                print(f"Response sent to {client_address}")

                # For demonstration, break after the first message
                #break
        except Exception as e:
            print(f"Error while receiving message: {e}")

    def close(self):
        """
        Close the UDP server socket.
        """
        self.server_socket.close()
        print("UDP Server socket closed.")


# Example usage:
if __name__ == "__main__":
    
    with open('configServer.json', 'r') as file:
        data = json.load(file)
        
    ip = data['Server']['ip']
    port = data['Server']['port']
    
    server = UDPServer(ip, port)
    server.listen()
    server.close()
