#Implement a client-server file transfer application where the client sends a file to the server using sockets. 
#Before transmitting the file, pickle the file object on the client side. On the server side, receive the pickled file object, unpickle it, and save it to disk.

#Requirements:
#The client should provide the file path of the file to be transferred.
#The server should specify the directory where the received file will be saved.
#Ensure error handling for file I/O operations, socket connections, and pickling/unpickling.


#SERVER.PY
import socket
import pickle
import os

# Server configuration
HOST = 'localhost'
PORT = 9999
SAVE_DIR = 'received_files'

# Ensure the save directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific host and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(1)

print("Server is listening...")

while True:
    # Accept connection from client
    client_socket, address = server_socket.accept()
    print(f"Connection from {address} has been established!")

    try:
        # Receive pickled file from the client
        serialized_file = client_socket.recv(4096)

        # Unpickle the file object
        file_data = pickle.loads(serialized_file)

        # Extract the filename from the file path
        filename = os.path.basename(file_data['filepath'])

        # Construct the path where the file will be saved
        save_path = os.path.join(SAVE_DIR, filename)

        # Write the received file to disk
        with open(save_path, 'wb') as file:
            file.write(file_data['content'])

        print(f"File received and saved as: {save_path}")

        # Send acknowledgment to the client
        client_socket.send(b'File received successfully!')

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the client connection
        client_socket.close()


#CLIENT.PY
import socket
import pickle

# Client configuration
HOST = 'localhost'
PORT = 9999

def send_file(filepath):
    try:
        # Open the file to be sent
        with open(filepath, 'rb') as file:
            # Read the file content
            content = file.read()

            # Prepare the data to be pickled
            file_data = {'filepath': filepath, 'content': content}

            # Serialize the file data
            serialized_file = pickle.dumps(file_data)

        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client_socket.connect((HOST, PORT))

        # Send the pickled file to the server
        client_socket.send(serialized_file)

        # Receive acknowledgment from the server
        ack = client_socket.recv(1024)
        print(ack.decode())

        # Close the socket
        client_socket.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    filepath = input("Enter the file path to be transferred: ")
    send_file(filepath)
