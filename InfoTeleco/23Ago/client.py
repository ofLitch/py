import socket
import threading
import json

# Define the fields
method = "HELLO"
usrc = "luna"
udst = "server"
msg = ""

# Create the JSON object
message_object = {
    "method": method,
    "usrc": usrc,
    "udst": udst,
    "msg": msg
}


class UDPClient:
    def __init__(self, server_ip, server_port):
        """
        Initialize the UDP Client with server IP and port.

        :param server_ip: The IP address of the server.
        :param server_port: The port number of the server.
        """
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listening = False
        print(f"UDP Client initialized for server at {self.server_ip}:{self.server_port}")

    def send_message(self, userDest, message):
        """
        Send a message to the server.

        :param message: The message to be sent (string).
        """
        try:
            fullMessage = message+"///"+userDest
            self.client_socket.sendto(fullMessage.encode('utf-8'), (self.server_ip, self.server_port))
            print(f"Message sent to {self.server_ip}:{self.server_port}")
        except Exception as e:
            print(f"Failed to send message: {e}")

    def _listen_for_messages(self, buffer_size=1024):
        """
        Private method to listen for messages from the server. Intended to run in a separate thread.

        :param buffer_size: The maximum amount of data to be received at once (default is 1024 bytes).
        """
        try:
            print("Started listening for messages from the server...")
            while self.listening:
                data, addr = self.client_socket.recvfrom(buffer_size)
                print(f"\nMessage received from {addr}: {data.decode('utf-8')}")
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


# Example usage:
if __name__ == "__main__":
    with open('configServer.json', 'r') as file:
        data = json.load(file)
        
    ip = data['Server']['ip']
    port = data['Server']['port']
    
    
    client = UDPClient(ip, port)

    # Start listening for messages from the server in a separate thread
    client.start_listening()

    # Continuously send messages from user input
    try:
        while True:
            message = json.dumps(message_object)
            
            client.send_message(message)
            userDest = input("Nombre del destinatario: ")
            message = input("Enter message to send to server (or type 'exit' to quit): ")
            #if message.lower() == 'exit':
            #    break
            client.send_message(userDest,message)
    except KeyboardInterrupt:
        print("\nClient interrupted.")

    # Close the client
    client.close()