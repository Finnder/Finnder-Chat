import socket
import threading
import tkinter as tk
import vidstream

LOCAL_IP = socket.gethostbyname(socket.gethostname())
IP = LOCAL_IP #'71.68.40.170'

PORT = 25566
FORMAT = 'ascii'
nickname = ''

MAIN_FONT = 'Terminal'
window_x = 700
window_y = 500
backgroundColor = 'gray13'
CurrentVersion = 0.1

# Checks If Your In A Specific Tab
inMessages = False

# Resets Window
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
    window.iconbitmap('Graphics/FCIcon.ico')

    # Look For Enter Keys - Starting Window
    def OnEnterPressed(event):
        LoadAreaSelectionWindow()

    window.bind('<Return>', OnEnterPressed)

    mainFrame = tk.Frame(window, bg="gray10")
    mainFrame.pack()

    errorLabel = tk.Label(mainFrame, text="", font=(MAIN_FONT, 11), fg='red', bg=backgroundColor)

    tk.Label(mainFrame, text=f"Successfully Connected To IP: {IP}", font=(MAIN_FONT, 19), fg='white', bg='SpringGreen').pack(pady=5)
    tk.Label(mainFrame, text="Enter A Nickname Below", font=(MAIN_FONT, 20), fg='white', bg=backgroundColor).pack(pady=10)

    def ErrorMessage(message):
        errorLabel.config(text=message)
        errorLabel.pack(pady=2)

    nickname_Entry = tk.Entry(mainFrame, font=(MAIN_FONT, 22))
    nickname_Entry.pack(pady=2)

    def LoadAreaSelectionWindow():
        # Checking For Requirements
        if nickname_Entry.get().split():
            if len(nickname_Entry.get()) >= 20:
                ErrorMessage("Character Length Is Over 20, Please Use A Shorter Nickname")
            else:
                AreaSelectionWindow()

        else:
            ErrorMessage("Nickname Entry Is Empty, Please Enter A Nickname")

    confirmButton = tk.Button(mainFrame, command=LoadAreaSelectionWindow, text="CONFIRM", font=(MAIN_FONT, 20))
    confirmButton.pack(pady=10)

    tk.Label(text="Version: " + str(CurrentVersion), font=(MAIN_FONT, 15), bg=backgroundColor, fg='white').pack(pady=15)
    window.mainloop()

def AreaSelectionWindow():
    global window
    SetUserNickname()
    RESET_WINDOW()

    # Look For Enter Keys - Area Selections
    def OnEnterPressed(event):
        pass

    window.bind('<Return>', OnEnterPressed)

    tk.Label(mainFrame, text="Select An Option Below", font=(MAIN_FONT, 25)).pack()

    ButtonSelection_TOP = tk.Frame(window, bg='gray10')
    ButtonSelection_TOP.pack(side=tk.BOTTOM, fill=tk.BOTH, pady=20)

    tk.Label(text="Sections", font=(MAIN_FONT, 15), bg=backgroundColor, fg='white').pack(in_=ButtonSelection_TOP, side=tk.TOP, pady=2)
    tk.Button(text="MESSAGING", command=LoadMessageWindow, font=(MAIN_FONT, 15), width=16, height=1).pack(in_=ButtonSelection_TOP, side=tk.LEFT, padx=4, pady=2)
    tk.Button(text="NUMBER THINGY", command=NumberWindow, font=(MAIN_FONT, 15), width=16, height=1).pack(in_=ButtonSelection_TOP, side=tk.LEFT, padx=4, pady=2)
    tk.Button(text="VOICE CHAT (WIP)", command=VoiceWindow, font=(MAIN_FONT, 15), width=16, height=1).pack(in_=ButtonSelection_TOP, side=tk.LEFT, padx=2, pady=2)

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

    # Look For Enter Keys - Message Window
    def OnEnterPressed(event):
        SendMessage()

    window.bind('<Return>', OnEnterPressed)

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

    def SendMessage():
        write() # Sends Message To -> Server -> All Clients
        ClearEntry()

    sendButton = tk.Button(mainFrame, command=SendMessage, text="SEND", font=(MAIN_FONT, 15), width=29, bg='SeaGreen1').pack(in_=chatButtonFrame, side=tk.LEFT, padx=2)
    clearButton = tk.Button(mainFrame, command=ClearMessages, text="CLEAR", font=(MAIN_FONT, 15), width=22, bg='SeaGreen4').pack(in_=chatButtonFrame, side=tk.LEFT)

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()

def NumberWindow():
    RESET_WINDOW()

def VoiceWindow():
    RESET_WINDOW()


    # Audio Server
    audio_receiver = vidstream.AudioReceiver(IP, PORT)

    # Start Listening To Audio
    def StartAudioListening():
        t1 = threading.Thread(target=audio_receiver.start_server)
        t1.start()

    def StartAudioSending():
        audio_sender = vidstream.AudioSender(IP, PORT)
        t3 = threading.Thread(target=audio_sender.start_stream)
        t3.start()

    def JOINCALL():
        print("Joined Call")
        StartAudioListening()
        StartAudioSending()


    def LEAVECALL():
        joinCallButton.config(text="JOIN CALL", fg='white', bg='green')
        joinCallButton.pack()

    # Deafen or Going off audio section
    def StopAudioListening():
        pass

    def MuteMic():
        pass

    tk.Label(mainFrame, text="Welcome To Voice Chat!", font=(MAIN_FONT, 30), bg=backgroundColor, fg='white').pack()

    audioOptionsArea = tk.Frame(mainFrame, bg='gray10')
    audioOptionsArea.pack(anchor=tk.CENTER)

    joinCallButton = tk.Button(mainFrame, text="JOIN CALL", command=JOINCALL, font=(MAIN_FONT, 12), bg='green', fg='white').pack(in_=audioOptionsArea)
    tk.Button(mainFrame, text="Mute", font=(MAIN_FONT, 10)).pack(in_=audioOptionsArea)
    tk.Button(mainFrame, text="Deafen", font=(MAIN_FONT, 10)).pack(in_=audioOptionsArea)

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

# Connection To Socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

StartingWindow()
