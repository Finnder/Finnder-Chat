import socket
import threading
import tkinter as tk

LOCAL_IP = socket.gethostbyname(socket.gethostname())
IP = LOCAL_IP  # '71.68.40.170'

PORT = 25566
FORMAT = 'ascii'
nickname = ''

MAIN_FONT = 'Terminal'
window_x = 700
window_y = 500
backgroundColor = 'gray13'
CurrentVersion = 0.1

inMessages = False


def RESET_WINDOW():
    global mainFrame
    global window
    global inMessages

    inMessages = False
    mainFrame.destroy()
    mainFrame = tk.Frame(window)
    mainFrame = tk.Frame(window, bg=backgroundColor)
    mainFrame.pack()


# What is sent to clients from server
def receive():
    global mainFrame
    global messages
    global client

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


def StartingWindow():
    global window
    global mainFrame
    global nickname_Entry
    global messagebox

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

    tk.Button(mainFrame, command=AreaSelectionWindow, text="CONFIRM", font=(MAIN_FONT, 20)).pack(pady=10)

    tk.Label(text="Version: " + str(CurrentVersion), font=(MAIN_FONT, 15), bg=backgroundColor, fg='white').pack(pady=15)
    window.mainloop()


def AreaSelectionWindow():
    SetUserNickname()
    RESET_WINDOW()

    tk.Label(mainFrame, text="Select An Option Below", font=(MAIN_FONT, 25)).pack()

    ButtonSelection_TOP = tk.Frame(window, bg='gray10')
    ButtonSelection_TOP.pack(side=tk.BOTTOM, fill=tk.BOTH, pady=20)

    tk.Label(text="Sections", font=(MAIN_FONT, 15), bg=backgroundColor, fg='white').pack(in_=ButtonSelection_TOP,
                                                                                         side=tk.TOP, pady=2)
    tk.Button(text="MESSAGING", command=LoadMessageWindow, font=(MAIN_FONT, 15), width=16, height=1).pack(
        in_=ButtonSelection_TOP, side=tk.LEFT, padx=4, pady=2)
    tk.Button(text="? (WIP)", command=NumberWindow, font=(MAIN_FONT, 15), width=16, height=1).pack(
        in_=ButtonSelection_TOP, side=tk.LEFT, padx=4, pady=2)
    tk.Button(text="VOICE CHAT (WIP)", command=VoiceWindow, font=(MAIN_FONT, 15), width=16, height=1).pack(
        in_=ButtonSelection_TOP, side=tk.LEFT, padx=2, pady=2)


def SetUserNickname():
    global nickname
    global userNickname
    userNickname = nickname_Entry.get()
    nickname = userNickname


def ClearMessages():
    MessageWindow()


def LoadMessageWindow():
    global inMessages
    if inMessages:
        pass
    else:
        MessageWindow()


def MessageWindow():
    global userMessage_var
    global window
    global messagebox
    global userNickname
    global nickname_Entry
    global messageArea
    global nickname
    global messages
    global inMessages

    # Reset
    RESET_WINDOW()
    inMessages = True

    nicknameText = f"Welcome, {userNickname}!"
    tk.Label(mainFrame, text=nicknameText, font=(MAIN_FONT, 20), bg=backgroundColor, fg='white').pack(pady=2)

    # Message Box
    messages = tk.Listbox(mainFrame, font=('Arial', 11), bg='gray10', fg='white')
    messages.pack(fill=tk.BOTH, pady=3)

    messagebox = tk.Entry(mainFrame, font=(MAIN_FONT, 20), width=33)
    messagebox.pack(pady=1)

    # Chat Buttons
    chatButtonFrame = tk.Frame(mainFrame, bg='gray10', pady=5)
    chatButtonFrame.pack(side=tk.TOP, fill=tk.BOTH)

    def ClearEntry():
        messagebox.delete(0, tk.END)

    sendButton = tk.Button(mainFrame, command=lambda: [write(), ClearEntry()], text="SEND", font=(MAIN_FONT, 15),
                           width=29, bg='SeaGreen1').pack(in_=chatButtonFrame, side=tk.LEFT, padx=2)
    clearButton = tk.Button(mainFrame, command=ClearMessages, text="CLEAR", font=(MAIN_FONT, 15), width=22,
                            bg='SeaGreen4').pack(in_=chatButtonFrame, side=tk.LEFT)

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()


def NumberWindow():
    RESET_WINDOW()
    tk.Label(mainFrame, text="? WIP", font=(MAIN_FONT, 30), bg=backgroundColor, fg='white').pack()


def VoiceWindow():
    RESET_WINDOW()
    tk.Label(mainFrame, text="Voice Chat WIP", font=(MAIN_FONT, 30), bg=backgroundColor, fg='white').pack()


# What is sent to the server from clients
def write():
    global userMessage
    global messagebox

    userMessage = messagebox.get()

    if userMessage.split():
        message = f'{nickname}: {userMessage}'
        client.send(message.encode(FORMAT))
    else:
        pass


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

StartingWindow()
