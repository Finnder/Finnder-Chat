import threading
import socket

LOCAL_IP = socket.gethostbyname(socket.gethostname())
host = ''
port = 25566
FORMAT = 'ascii'
nickname = ''

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    global nickname

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
            print(f'{nickname} Has Left The Chat Room!')
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected With {str(address)}")

        client.send('NICK'.encode(FORMAT))

        try:
            nickname = client.recv(1024).decode(FORMAT)
        except:
            print("Error With Nickname")
            continue

        # ADD New User To Arrays
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname Of The Client Is {nickname}!')
        broadcast(f'{nickname} Joined The Chat!'.encode(FORMAT))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("===== FINNDER CHAT SERVER (0.1) =====")
print("Server Is Now Listening For Connections...")
receive()
