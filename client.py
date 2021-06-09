import socket
import threading
import tkinter as tk

IP = '71.68.40.170'
PORT = 25565
FORMAT = 'ascii'

MAIN_FONT = 'Terminal'
window_x = 700
window_y = 500


def RESET_WINDOW():
    global mainFrame
    global window

    mainFrame.destroy()
    mainFrame = tk.Frame(window)
    mainFrame = tk.Frame(window, bg="gray10")
    mainFrame.pack()


def StartingWindow():
    global window
    global mainFrame
    global nickname_Entry

    window = tk.Tk()
    window.geometry(f"{window_x}x{window_y}")
    window.resizable(False, False)
    window.configure(background='gray10')
    window.title("Finnder Chat")

    mainFrame = tk.Frame(window, bg="gray10")
    mainFrame.pack()

    tk.Label(mainFrame, text=f"Successfully Connected To IP: {IP}", font=(MAIN_FONT, 10), fg='GREEN').pack(pady=2)
    tk.Label(mainFrame, text="Enter A Nickname Below").pack(pady=2)

    nickname_Entry = tk.Entry(mainFrame, font=(MAIN_FONT, 20))
    nickname_Entry.pack(pady=2)
    tk.Button(mainFrame, command=MainClientWindow, text="CONFIRM", font=(MAIN_FONT, 20)).pack(pady=2)
    window.mainloop()

# What is sent to clients from server
def receive():
    global mainFrame
    while True:
        try:
            message = client.recv(1024).decode(FORMAT)
            if message == 'NICK':
                client.send(nickname.encode(FORMAT))
            else:
                # Final Send to all clients
                tk.Label(mainFrame, text=f"{message}").pack(padx=2, pady=1)

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

    userNickname = nickname_Entry.get()
    nickname = userNickname

    # Reset
    RESET_WINDOW()

    nicknameText = f"Welcome, {userNickname}!"
    tk.Label(mainFrame, text=nicknameText, font=(MAIN_FONT, 20)).pack(pady=2)
    messagebox = tk.Entry(mainFrame, font=(MAIN_FONT, 20))
    messagebox.pack(pady=1)
    sendButton = tk.Button(mainFrame, command=write, text="Send Message | sc: enter", font=(MAIN_FONT, 20))
    sendButton.pack(pady=1)

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

StartingWindow()
