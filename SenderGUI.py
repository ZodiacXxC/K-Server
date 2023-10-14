import customtkinter as ctk
import tkinter as tk
import socket
import threading
import time
import tkinter.messagebox as tkmb 

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

appWidth, appHeight = 500, 500
response = ""
datax = None

def login():
    username = valueEntry.get()
    password = propEntry.get()

    global commandOptionMenu
    global processOptionMenu
    global startButton
    global textbox
    if username == "tareq" and password == "tareq112233":
        tkmb.showinfo(title="Login Successful",message="You have logged in Successfully")
        valueEntry.destroy()
        valueLabel.destroy()
        propEntry.destroy()
        propLabel.destroy()
        logButton.destroy()
        commandLabel = ctk.CTkLabel(app, text="Command:")
        commandLabel.grid(row=8, column=0, padx=20, pady=20, sticky="ew")


        commandOptions = ["Kill", "Run", "Shutdown", "Restart"]

        commandOptionMenu = ctk.CTkOptionMenu(app ,values=commandOptions,command=changeOptions)
        commandOptionMenu.grid(row=8, column=1, padx=20, pady=20, columnspan=2, sticky="ew")


        processLabel = ctk.CTkLabel(app, text="Process:")
        processLabel.grid(row=9, column=0, padx=20, pady=20, sticky="ew")

        processOptions = ["AlSahlHIS", "Chrome", "Notepad"]
        processOptionMenu = ctk.CTkOptionMenu(app, values=processOptions)
        processOptionMenu.grid(row=9, column=1, padx=20, pady=20, columnspan=2, sticky="ew")

        startButton = ctk.CTkButton(app, text="Start a command", command=startCommand)
        startButton.grid(row=10, column=1, columnspan=2, padx=20, pady=20, sticky="ew")
        startButton.configure(state="disabled")

        textbox = ctk.CTkTextbox(app,width=280, height=60)
        textbox.grid(row=11, column=1, columnspan=2, padx=20, pady=20, sticky="ew")
        # Create a thread to handle server connections
        server_thread = threading.Thread(target=TryCon)
        server_thread.start()
    else:
        tkmb.showinfo(title="Login failed",message="Incorrect username or password , Please try again !!")
def startCommand():
    global response
    command_value = commandOptionMenu.get()
    process_value = processOptionMenu.get()
    if command_value == "Kill":
        process_value = process_value + ".exe"
        response = f"taskkill /IM {process_value} /F"
        sendCommandThread = threading.Thread(target=sendCommand)
        sendCommandThread.start()
    elif command_value == "Run" :
        if process_value == "AlSahlHIS" :
            response = "C:\\Users\\USER\\Desktop\\AlSahlHIS .exe - Shortcut.lnk"
            sendCommandThread = threading.Thread(target=sendCommand)
            sendCommandThread.start()
        else:
            response = f"start {process_value}"
            sendCommandThread = threading.Thread(target=sendCommand)
            sendCommandThread.start()
    elif command_value == "Shutdown" :
        response = "shutdown /f /t 30"
        sendCommandThread = threading.Thread(target=sendCommand)
        sendCommandThread.start()
    elif command_value == "Restart" :
        response = "shutdown /f /r /t 30"
        sendCommandThread = threading.Thread(target=sendCommand)
        sendCommandThread.start()

def sendCommand():
    global response
    try:
        sock.send(response.encode("utf-8"))
    except Exception as e:
        print("Error sending command:", str(e))



def changeOptions(select_options):
    if select_options == "Shutdown" or select_options == "Restart":
        processOptions = []
        processOptionMenu.configure(values=processOptions)
        processOptionMenu.set("")


    elif select_options == "Kill" or select_options == "Run" :
        processOptions = ["AlSahlHIS", "Chrome", "Notepad"]
        processOptionMenu.configure(values=processOptions)
        processOptionMenu.set("AlSahlHIS")

def move_to_next(event):
    event.widget.tk_focusNext().focus_set()

def move_to_login(event):
    login()


app = ctk.CTk()
app.title("K-Server")
app.geometry(f"{appWidth}x{appHeight}")

programLabel = ctk.CTkLabel(app,text="K-Server",font=("Times New Roman", 36))
programLabel.grid(row=0, column=1, padx=100, pady=20, sticky="ew")
# Value form
valueLabel = ctk.CTkLabel(app, text="Username:", font=("Arial", 12, "bold"))
valueLabel.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

valueEntry = ctk.CTkEntry(app,placeholder_text="Username")
valueEntry.grid(row=1, column=1, padx=20, pady=20, sticky="ew")
valueEntry.bind("<Return>", move_to_next)

# Proportion form
propLabel = ctk.CTkLabel(app, text="Password:", font=("Arial", 12, "bold"))
propLabel.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

propEntry = ctk.CTkEntry(app,placeholder_text="Username",show="*")
propEntry.grid(row=2, column=1, padx=20, pady=20, sticky="ew")
propEntry.bind("<Return>", move_to_login)

#login form 
logButton = ctk.CTkButton(app, text="Login", command=login)
logButton.grid(row=3, column=1, columnspan=2, padx=20, pady=20, sticky="ew")



host = "192.160.0.138"
port = 12345



def receive(socket, signal):
    while signal:
        try:
            data = socket.recv(32)
            if not data:
                break
            print(data.decode('utf-8'))
        except:
            socket.close()
            TryCon()

def TryCon():
    global datax
    while True:
        try:
            global sock
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            textbox.delete(1.0, "end")
            textbox.insert("end","Server connect...\n")
            startButton.configure(state="normal")
            datax = True
            break
        except:
            textbox.insert("end","Server not available. Retrying in 1 second...\n")
            startButton.configure(state="disabled")
            datax = False
            time.sleep(1)
    StartCon()

def StartCon():
    receiveThread = threading.Thread(target=receive, args=(sock, True))
    receiveThread.start()
    while True:
        if datax:
            time.sleep(5)
            pass
        else:
            break



app.mainloop()
