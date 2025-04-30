import socket
import threading

alias = input("Enter your alias: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == 'ALIAS':
                client.send(alias.encode())
            else:
                print(message)
        except:
            print("An error occurred.")
            client.close()
            break

def send_messages():
    while True:
        message = f"{alias}: {input('')}"
        client.send(message.encode())

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
