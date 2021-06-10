import socket
import threading
import tkinter as tk

LOCAL_IP = socket.gethostbyname(socket.gethostname())
IP = '71.68.40.170'

PORT = 25565
FORMAT = 'ascii'

MAIN_FONT = 'Terminal'
window_x = 700
window_y = 500
backgroundColor = 'gray13'

CurrentVersion = 0.1


def RESET_WINDOW():
    global mainFrame
    global window

    mainFrame.destroy()
    mainFrame = tk.Frame(window)
    mainFrame = tk.Frame(window, bg=backgroundColor)
    mainFrame.pack()


def StartingWindow():
    global window
    global mainFrame
    global nickname_Entry

    window = tk.Tk()
    window.geometry(f"{window_x}x{window_y}")
    window.resizable(False, False)
    window.configure(background=backgroundColor)
    window.title("Finnder Chat")

    mainFrame = tk.Frame(window, bg="gray10")
    mainFrame.pack()

    tk.Label(mainFrame, text=f"Successfully Connected To IP: {IP}", font=(MAIN_FONT, 19), fg='white',
             bg='SpringGreen').pack(pady=5)
    tk.Label(mainFrame, text="Enter A Nickname Below", font=(MAIN_FONT, 20), fg='white', bg=backgroundColor).pack(
        pady=10)

    nickname_Entry = tk.Entry(mainFrame, font=(MAIN_FONT, 22))
    nickname_Entry.pack(pady=2)

    tk.Button(mainFrame, command=MainClientWindow, text="CONFIRM", font=(MAIN_FONT, 20)).pack(pady=10)

    versionLabel = tk.Label(text="Version: " + str(CurrentVersion), font=(MAIN_FONT, 15), bg=backgroundColor,fg='white').pack(pady=15)
    window.mainloop()


# What is sent to clients from server
def receive():
    global mainFrame
    global messages

    while True:
        try:
            message = client.recv(1024).decode(FORMAT)
            if message == 'NICK':
                client.send(nickname.encode(FORMAT))
            else:
                messages.insert(tk.END, f'{message}')

        except:
            print('An Error Occurred')
            client.close()
            break


# What is sent to the server from clients
def write():
    global userMessage
    global messagebox
    userMessage = messagebox.get()
    message = f'{nickname}: {userMessage}'
    client.send(message.encode(FORMAT))


def MainClientWindow():
    global userMessage_var
    global window
    global messagebox
    global userNickname
    global nickname_Entry
    global messageArea
    global nickname
    global messages

    userNickname = nickname_Entry.get()
    nickname = userNickname

    # Reset
    RESET_WINDOW()

    nicknameText = f"Welcome, {userNickname}!"
    tk.Label(mainFrame, text=nicknameText, font=(MAIN_FONT, 20), bg=backgroundColor, fg='white').pack(pady=2)
    messagebox = tk.Entry(mainFrame, font=(MAIN_FONT, 20))
    messagebox.pack(pady=1)

    sendButton = tk.Button(mainFrame, command=write, text="Send", font=(MAIN_FONT, 20))
    sendButton.pack(pady=1)

    # Message Box
    messages = tk.Listbox(mainFrame, font=('Arial', 12), bg='gray')
    messages.pack(fill=tk.BOTH, pady=3)

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

StartingWindow()
