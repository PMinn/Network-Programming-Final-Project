####################################################
#  Network Programming - Unit 2 Simple TCP Client Server Program         
#  Program Name: 3-TCPClient.py                                      			
#  The program is a simple TCP client.            		
#  2021.07.13                                                   									
####################################################
import sys
import socket
import threading
import tkinter as tk
import tkinter.simpledialog as sd

PORT = 6666
BUF_SIZE = 1024			# Receive buffer size

class Dialog(sd.Dialog):
    def __init__(self, parent, title, text):
        self.text = text
        super().__init__(parent, title)
        
    def body(self, frame):
        tk.Label(frame, text = self.text, justify = 'left', width = 50, pady = 10).pack()

    def buttonbox(self):
        self.ok__button = tk.Button(self, text = '好', command = self.ok_pressed, default = 'active', width = 5)
        self.ok__button.pack(side = 'bottom', pady = 10, expand = True)

    def ok_pressed(self):
        self.destroy()

class ClientThread(threading.Thread):
    def __init__(self, cSocket):
        super().__init__()
        self.cSocket = cSocket
        self.start()

    def run(self):
        client_msg = self.cSocket.recv(BUF_SIZE)
        while client_msg:
            data  = client_msg.decode('utf-8')
            while data[len(data) - 1] != '\0':
                client_msg = self.cSocket.recv(BUF_SIZE)
                data += client_msg.decode('utf-8')
            
            data = data.split('^^')
            print(data[2])
            print(f'from: {data[1]}\n------------')
            client_msg = self.cSocket.recv(BUF_SIZE)

class LoginWindow(tk.Tk):
    def __init__(self, title):
        super().__init__(title)
        self.geometry("400x300")

        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 2)

        ipLabel = tk.Label(self ,text = "server IP")
        ipLabel.grid(row = 0, column = 0)
        self.ipEntry = tk.Entry(self)
        self.ipEntry.grid(row = 0, column = 1)
        self.ipEntry.insert(0, '127.0.0.1')

        accountLabel = tk.Label(self ,text = "名稱")
        accountLabel.grid(row = 1, column = 0)
        self.accountEntry = tk.Entry(self)
        self.accountEntry.grid(row = 1, column = 1)

        self.start_btn = tk.Button(self, text='連線', command = lambda:serverConnecting(self))
        self.start_btn.grid(row = 2, column = 0,columnspan = 2, pady = 20)#, sticky = "WENS"
        self.mainloop()

def serverConnecting(window):
    window.start_btn["state"] = tk.DISABLED
    serverIP = socket.gethostbyname(window.ipEntry.get())

    try:
        print('Connecting to %s port %s' % (serverIP, PORT))
        cSocket.connect((serverIP, PORT))
    except socket.error as e:
        window.start_btn["state"] = tk.NORMAL
        Dialog(window, 'Socket error', str(e))
        print('Socket error: %s' % str(e))
        return
    except Exception as e:
        window.start_btn["state"] = tk.NORMAL
        print('Other exception: %s' % str(e))
        Dialog(window, 'Other exception', str(e))
        return 
    serverStart()

def serverStart():
    ClientThread(cSocket)
    try:
        while(1):
            msg = str(input())
            print('from: me\n------------')
            cmd = f"message^^%id%^^{msg}\0"
            #sys.getsizeof(msg)
            cSocket.send(cmd.encode('utf-8'))
    except socket.error as e:
        print('Socket error: %s' % str(e))
    except Exception as e:
        print('Other exception: %s' % str(e))
    finally:
        print('Closing connection.')
            # Close the TCP socket
    #cSocket.close()

cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
window = LoginWindow("123456")
