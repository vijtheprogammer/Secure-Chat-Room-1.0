import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to localhost and port 9990
server_socket.bind(('localhost', 9990))

# Listen for incoming connections, with a maximum backlog of 5 connections
server_socket.listen(5)

print("Server listening for incoming connections....")

try:
    # Main loop to accept incoming connections
    while True:
        try:
            # Accept a new connection
            client_socket, addr = server_socket.accept()
            print("Got connection from", addr)
            
            # Send SYN-ACK to client to initiate the three-way handshake
            client_socket.send(b"SYN-ACK")
            
            # Wait for ACK from client to complete the three-way handshake
            ack = client_socket.recv(1024)
            if ack == b"ACK":
                print("\nConnection established successfully!")
            
            # Generate a random 32-byte key for AES-256 encryption
            key = os.urandom(32)
            
            # Inner loop to handle communication with the connected client
            while True:
                # Receive data from client
                data = client_socket.recv(1024)
                
                # If no data received, break the loop and close the connection
                if not data:
                    print("Client disconnected.")
                    break
                
                # Decrypt the received data using AES-256
                cipher = Cipher(algorithms.AES(key), modes.CTR(os.urandom(16)), backend=default_backend())
                decryptor = cipher.decryptor()
                decrypted_message = decryptor.update(data) + decryptor.finalize()
                
                # Print the encrypted message in hexadecimal format
                print("Received (hex):", decrypted_message.hex())
                
                # Get user input for response
                response = input("\nEnter response: ")
                
                # Encrypt the response using AES-256
                cipher = Cipher(algorithms.AES(key), modes.CTR(os.urandom(16)), backend=default_backend())
                encryptor = cipher.encryptor()
                encrypted_response = encryptor.update(response.encode()) + encryptor.finalize()
                
                # Send the encrypted response back to client
                client_socket.send(encrypted_response)
            
            # Close the client socket after communication
            client_socket.close()
        except KeyboardInterrupt:
            # Handle KeyboardInterrupt gracefully by printing a message and closing the server socket
            print("\nServer shutting down...")
            server_socket.close()
            break
        except ConnectionResetError:
            print("Client forcibly closed the connection.")
except OSError as e:
    # Handle OSError (e.g., "Bad file descriptor") by printing the error message
    print(e)