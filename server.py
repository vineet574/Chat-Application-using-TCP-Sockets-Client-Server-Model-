import socket
import threading

host = '127.0.0.1'
port = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
aliases = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f"{alias} has left the chat.".encode())
            aliases.remove(alias)
            break

def receive():
    print("Server is running and listening...")
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("ALIAS".encode())
        alias = client.recv(1024).decode()
        aliases.append(alias)
        clients.append(client)

        print(f"Alias of the client is {alias}")
        broadcast(f"{alias} has joined the chat.".encode())
        client.send("You are now connected!".encode())

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()
