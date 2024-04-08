import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def main():
    try:
        # Create a TCP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server running on localhost and port 9990
        client_socket.connect(("localhost", 9990))

        # Wait for SYN-ACK from the server to initiate the three-way handshake
        syn_ack = client_socket.recv(1024)
        
        # If SYN-ACK received, send ACK to complete the three-way handshake
        if syn_ack == b"SYN-ACK":
            client_socket.send(b"ACK")
            print("\nHandshake completed. Connection established!")
        
        # Generate a random 32-byte key for AES-256 encryption
        key = os.urandom(32)
        
        # Main loop for sending and receiving messages
        while True:
            # Get user input for message
            message = input("\nEnter message (Type '^C' to quit): ")
            
            # Check if the user wants to quit
            if message == "^C":
                print("Quitting...")
                break
            
            # Encrypt the message using AES-256
            cipher = Cipher(algorithms.AES(key), modes.CTR(os.urandom(16)), backend=default_backend())
            encryptor = cipher.encryptor()
            encrypted_message = encryptor.update(message.encode()) + encryptor.finalize()
            
            # Send the encrypted message to the server
            client_socket.send(encrypted_message)
            
            # Receive response from the server
            response = client_socket.recv(1024)
            
            # Decrypt the response using AES-256
            decryptor = cipher.decryptor()
            decrypted_response = decryptor.update(response) + decryptor.finalize()
            
            # Print the decrypted response in hexadecimal format
            print("Server response (hex):", decrypted_response.hex())

    except ConnectionRefusedError:
        print("Server is not online. Please try again later.")
    except KeyboardInterrupt:
        # Handle KeyboardInterrupt gracefully by printing a message and closing the client socket
        print("\nClient shutting down...")
    finally:
        # Close the client socket
        client_socket.close()

if __name__ == "__main__":
    main()
