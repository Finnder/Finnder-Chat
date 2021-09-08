import tkinter as tk


def sendMSG(listbox, msg, *color):
    listbox.insert(tk.END, msg)
    listbox.itemconfig(tk.END, {'fg': color})

def Menu(listbox):
    ClearListbox(listbox)
    sendMSG(listbox, 'WELCOME TO FINNDERS RPG!', 'red')
    sendMSG(listbox, 'Continue A Game', 'yellow')
    sendMSG(listbox, 'Start A *NEW* Game', 'orange')
    sendMSG(listbox, 'Leaderboards', 'grey')
    sendMSG(listbox, 'Options')

def CharacterCreation(listbox):
    ClearListbox(listbox)
    sendMSG(listbox, 'What is your name?', 'orange')

def ClearListbox(listbox):
    listbox.delete(0, tk.END)