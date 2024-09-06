import socket
import threading
import rsa
import pickle
import json

file_pri_c2 = open('pri_key_client2.txt', 'rb')
private_key_c2 = pickle.load(file_pri_c2)
file_pri_c2.close()

file_pub_c = open('pub_key_client.txt', 'rb')
public_key_c = pickle.load(file_pub_c)
file_pub_c.close()

#Data receiver
data_receiver = {

    "ip_address":"127.0.0.0",
    "port": "12000"

}


class UDPClient:
    def __init__(self, server_ip, server_port, client2_ip,client2_port):
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
        self.listening = False
        print(f"UDP Client initialized for server at {self.server_ip}:{self.server_port}")

    def send_message(self, message = None):
        """
        Send a message to the server.

        :param message: The message to be sent (string).
        """
        ip_client2 = self.client2_ip.encode('utf-8')
        port_client2 = str(self.client2_port).encode('utf-8')
        try:
            #encrypt the message
            enc_message = rsa.encrypt(message.encode(), private_key_c2)
            self.client_socket.sendto(enc_message, (self.server_ip, self.server_port))

            if message:

                self.client_socket.sendto(ip_client2,(self.server_ip, self.server_port))
                self.client_socket.sendto(port_client2,(self.server_ip, self.server_port))
            #self.client_socket.sendto(message.encode('utf-8'), (self.server_ip, self.server_port))
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
                # data, addr = self.client_socket.recvfrom(buffer_size)
                # print(f"\nMessage received from {addr}: {data.decode('utf-8')}")

                data, client_address = self.client_socket.recvfrom(buffer_size)
                print(data)
                dec_message = rsa.decrypt(data, public_key_c).decode()
                print(dec_message)
                # message = data.decode('utf-8')
                print(f"Received message from {client_address}: {dec_message}")

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
    client = UDPClient("127.0.0.1", 12000,"127.0.0.1", 12000)

    # Start listening for messages from the server in a separate thread
    client.start_listening()

    # Continuously send messages from user input
    try:
        while True:
            message = input("Enter message to send to server (or type 'exit' to quit): ")
            if message.lower() == 'exit':
                break
            client.send_message(message)
    except KeyboardInterrupt:
        print("\nClient interrupted.")

    # Close the client
    client.close()