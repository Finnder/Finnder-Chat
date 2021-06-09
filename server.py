import threading
import socket

host = '71.68.40.170'
port = 5052
FORMAT = 'ascii'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} Has Left The Chat!'.encode(FORMAT))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected With {str(address)}")

        client.send('NICK'.encode(FORMAT))
        nickname = client.recv(1024).decode(FORMAT)

        # ADD New User To Arrays
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname Of The Client Is {nickname}!')
        broadcast(f'{nickname} Joined The Chat!'.encode(FORMAT))
        client.send('Connected To The Server!'.encode(FORMAT))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server Is Now Listening For Connections...")
receive()
