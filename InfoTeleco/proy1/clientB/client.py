import socket
import threading
import rsa
import pickle
from pathlib import Path



class UDPClient:
    def __init__(self, server_ip, server_port, local_ip, local_port):
        """
        Initialize the UDP Client with server IP and port.

        :param server_ip: The IP address of the server.
        :param server_port: The port number of the server.
        """
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.bind((local_ip, local_port))
        self.listening = False
        
        self.priKey = ""
        self.pubKey = ""
        self.pubKeyA = ""
        
        print(f"UDP Client initialized for server at {self.server_ip}:{self.server_port}")

    def send_message(self, message):
        """
        Send a message to the server.

        :param message: The message to be sent (string).
        """
        try:
            #encrypt the message
            enc_message = self.encryptMsg(message)
            self.client_socket.sendto(enc_message, (self.server_ip, self.server_port))
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
                data, addr = self.client_socket.recvfrom(buffer_size)
                msg = rsa.decrypt(data, self.pubKeyA).decode()
                print(f"\nMessage received from {addr}: {msg.decode('utf-8')}")
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
        
    # Maniobrar Msg
    def encryptMsg(self, msg):
        return rsa.encrypt(msg.encode(), self.priKey)
    
    def decryptMsg(self, data):
        return rsa.decrypt(data, self.pubKey).decode()
    
    # For keys
    def generateKeys(self):
        private_key, public_key = rsa.newkeys(512)
        file_pri = open('clientB/privKeyUserB.txt', 'wb')
        pickle.dump(private_key, file_pri)
        file_pri.close()

        file_pub = open('clientB/pubKeyUserB.txt', 'wb')
        pickle.dump(public_key, file_pub)
        file_pub.close()
        
    def readKeys(self):
        file_pri_c = open('clientB/privKeyUserB.txt', 'rb')
        self.priKey = pickle.load(file_pri_c)
        file_pri_c.close()
        
        file_pub_c = open('clientB/pubKeyUserB.txt', 'rb')
        self.pubKey = pickle.load(file_pub_c)
        file_pub_c.close()
        
        file_pub_c_A = open('clientB/pubKeyUserA.txt', 'rb')
        self.pubKeyA = pickle.load(file_pub_c_A)
        file_pub_c_A.close()


        
    def requestKeyFromUser(self):
        try:
            msg = "¡publicKeyFromA!##" + self.pubKey
            enc_msg = self.encryptMsg(msg)
            self.client_socket.sendto(enc_msg, (self.server_ip, self.server_port))
            
            self.listening = True
            response = ""
            while self.listening:
                data, addr = self.client_socket.recvfrom(buffer_size = 1024)
                response = data.decode('utf-8')
            self.listening = False
            self.saveKeyFromUser(response)
        except Exception as e:
            print(f"Failed to send msg: {e}")
            
    def saveKeyFromUser(public_key):
        file_pub = open('clientB/pubKeyUserA.txt', 'wb')
        pickle.dump(public_key, file_pub)
        file_pub.close()
    
    def readKeyFromUser():
        file_pub = open('clientB/pubKeyUserA.txt', 'rb')
        key = pickle.load(file_pub)
        file_pub.close()
        return key


# Example usage:
if __name__ == "__main__":
    
    client = UDPClient("127.0.0.1", 12000, "127.0.0.1", 53592)
    # Start listening for messages from the server in a separate thread
    client.start_listening()
    
    file_pri = Path('privKeyUser.txt')
    file_pub = Path('pubKeyUser.txt')
    #file_pub_other_user = Path('clientB/pubKeyUserA.txt')
    
    if not (file_pri.is_file() and file_pub.is_file()):
        client.generateKeys()
    client.readKeys()
    
    """ if not (file_pub_other_user.is_file()):
        client.requestKeyFromUser() """


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