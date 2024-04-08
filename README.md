# Secure Chat Room (Version 1.0)

These two scripts constitute a basic client-server communication system with encryption using AES-256 in Counter (CTR) mode. Let's break down the functionality of each script:

**client.py:**

1. Imports necessary modules including socket for networking and cryptography for encryption.
2. Defines the main() function which does the following:
- Creates a TCP socket.
- Connects to a server running on localhost at port 9990.
- Completes the three-way handshake by sending SYN-ACK and receiving ACK.
- Generates a random 32-byte key for AES-256 encryption.
    - Enters a loop to send and receive encrypted messages:
    - Gets user input for a message.
    - Encrypts the message using AES-256.
    - Sends the encrypted message to the server.
    - Receives a response from the server.
    - Decrypts the response using AES-256.
    - Prints the decrypted response in hexadecimal format.
- Gracefully handles errors including ConnectionRefusedError and KeyboardInterrupt.
- Finally, closes the client socket.

**server.py:**

1. Imports necessary modules.
2. Creates a TCP socket, binds it to localhost at port 9990, and starts listening for incoming connections.
3. Enters a loop to accept incoming connections:
- Accepts a new connection.
- Sends SYN-ACK to initiate the three-way handshake and waits for ACK to complete it.
- Generates a random 32-byte key for AES-256 encryption.
- Enters an inner loop to handle communication with the connected client:
    - Receives encrypted data from the client.
    - Decrypts the data using AES-256.
    - Prints the decrypted message in hexadecimal format.
    - Gets user input for a response.
    - Encrypts the response using AES-256.
    - Sends the encrypted response back to the client.
- Closes the client socket after communication.

4. Gracefully handles errors including KeyboardInterrupt and ConnectionResetError.
5. In case of an OSError, prints the error message.


Overall, this code establishes a secure communication channel between a client and a server using AES-256 encryption, ensuring that messages sent between them are encrypted and decrypted securely.
