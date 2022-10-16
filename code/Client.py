####################################################
#  Network Programming - Unit 2 Simple TCP Client Server Program         
#  Program Name: 3-TCPClient.py                                      			
#  The program is a simple TCP client.            		
#  2021.07.13                                                   									
####################################################
#import sys
import socket
import threading
import tkinter as tk
import tkinter.simpledialog as sd
import tkinter.font as tkFont
import math

PORT=6666
BUF_SIZE=1024			# Receive buffer size

class RoundedCanvas(tk.Canvas):
    def __init__(self, parent, border_radius, padding, bgc, color="black", height=-1, width=-1, maxWidth=-1, text='', command=None, cursor="arrow"):
        self.font=tkFont.Font(size=10, family='Helvetica')
        lineheight=self.font.metrics()['linespace']
        textWidth=self.font.measure(text)
        if height == -1:
            height=lineheight + (2 * padding)
        if width == -1:
            width=textWidth + (2 * padding)
        maxTextWidth=maxWidth - (2 * padding)
        if maxTextWidth < textWidth and maxWidth != -1:
            height=lineheight*math.ceil(textWidth/maxTextWidth) + (2 * padding)
            width=maxWidth
            
        #width=width if width >= 80 else 80
        tk.Canvas.__init__(self, parent, borderwidth=0, relief="raised", highlightthickness=0, bg=parent["bg"], cursor=cursor)
        self.id=None
        if border_radius > 0.5*width:
          print("Error: border_radius is greater than width.")
          return None
        if border_radius > 0.5*height:
          print("Error: border_radius is greater than height.")
          return None
        rad=2*border_radius
        
        def shape():
          self.create_arc((0, rad, rad, 0), start=90, extent=90, fill=bgc, outline=bgc)
          self.create_arc((width-rad, 0, width, rad), start=0, extent=90, fill=bgc, outline=bgc)
          self.create_arc((width, height-rad, width-rad, height), start=270, extent=90, fill=bgc, outline=bgc)
          self.create_arc((0, height-rad, rad, height), start=180, extent=90, fill=bgc, outline=bgc)
          return self.create_polygon((0, height-border_radius, 0, border_radius, border_radius, 0, width-border_radius, 0, width, border_radius, width, height-border_radius, width-border_radius, height, border_radius, height), fill=bgc, outline=bgc)
        self.id=shape()
        self.create_text(width/2, height/2, text=text, fill=color, font=self.font, width=maxTextWidth)
        (x0, y0, x1, y1)=self.bbox("all")
        width=(x1-x0)
        height=(y1-y0)
        self.configure(width=width, height=height)
          
class RadiusButton(RoundedCanvas):
    def __init__(self, parent, border_radius, padding, bgc, color="black", height=-1, width=-1, text='', command=None):
        self.command=command
        super().__init__(parent, border_radius=border_radius, padding=padding, bgc=bgc, color=color, height=height, width=width, text=text, cursor="hand2")
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_release(self, event):
      if self.command is not None and self["state"] == tk.NORMAL:
          self.command()

class Dialog(sd.Dialog):
    def __init__(self, parent, title, text):
        self.text=text
        super().__init__(parent, title)
        
    def body(self, frame):
        tk.Label(frame, text=self.text, justify='left', width=50, pady=10).pack()

    def buttonbox(self):
        self.ok__button=tk.Button(self, text='好', command=self.ok_pressed, default='active', width=5)
        self.ok__button.pack(side='bottom', pady=10, expand=True)

    def ok_pressed(self):
        self.destroy()

class LoginWindow(tk.Tk):
    def __init__(self, title):
        super().__init__(title)
        self.bgc="#161819"
        self.color="#fff"
        self.selectbackground="#555555"
        self.input_bgc="#1D1F20"
        self.geometry("400x300")
        self.configure(bg=self.bgc)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        plane=tk.Frame(self, bg=self.bgc)
        plane.place(relx=0.5, rely=0.5, anchor="center")
        ipLabel=tk.Label(plane ,text="server IP", bg=self.bgc, fg=self.color)
        ipLabel.grid(row=0, column=0, padx=10, pady=10)
        self.ipEntry=tk.Entry(plane, bg=self.input_bgc, fg=self.color, highlightthickness=1, highlightcolor=self.selectbackground, highlightbackground=self.selectbackground, insertbackground=self.color)
        self.ipEntry.config(selectbackground=self.selectbackground, bd=0)
        self.ipEntry.grid(row=0, column=1, padx=10, pady=10)
        self.ipEntry.insert(0, '127.0.0.1')

        accountLabel=tk.Label(plane ,text="名稱", bg=self.bgc, fg=self.color)
        accountLabel.grid(row=1, column=0, padx=10, pady=10)
        self.accountEntry=tk.Entry(plane, bg=self.input_bgc, fg=self.color, highlightthickness=1, highlightcolor=self.selectbackground, highlightbackground=self.selectbackground, insertbackground=self.color)
        self.accountEntry.config(selectbackground=self.selectbackground, bd=0)
        self.accountEntry.grid(row=1, column=1, padx=10, pady=10)

        # self.start_btn=tk.Button(plane, text='連線', command=lambda:serverConnecting(self))
        self.start_btn=RadiusButton(plane, text="連線", border_radius=4, padding=10, command=lambda:serverConnecting(self), bgc="#EC6D46", color="#fff")
        self.start_btn.grid(row=2, column=0,columnspan=2, pady=20)#, sticky="WENS"
        self.mainloop()

class GameWindow(tk.Toplevel):
    def __init__(self, account):
        super().__init__()
        self.title(account)
        self.geometry("1000x563")
        self.protocol("WM_DELETE_WINDOW", self.exit)
        tk.Frame(self).pack(side="left", fill="both", expand=True)
        self.chatRoom=ChatRoom(self)
        self.chatRoom.pack(side="right", fill="y", expand=False)

        '''
        menubar=tk.Menu(self)
        menubar.add_cascade(label="刷新信箱", command=self.refresh)
        menubar.add_cascade(label="復原刪除信件", command=self.reset)
        self.configure(menu=menubar)
        '''
    def exit(self):
        self.destroy()

class ScrollableFrame(tk.Frame):
    def __init__(self, parent, bgc):
        super().__init__(parent)
        vscrollbar=tk.Scrollbar(self, orient='vertical')
        vscrollbar.pack(fill='y', side='right', expand=False)
        self.canvas=tk.Canvas(self, bd=0, yscrollcommand=vscrollbar.set, bg=bgc, highlightthickness=0)
        vscrollbar.config(command=self.canvas.yview)
        self.frame=tk.Frame(self.canvas, bg=bgc, width=parent.winfo_reqwidth())
        self.frame.bind("<Configure>", self.resize_scrollregion)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.config(yscrollcommand=vscrollbar.set)
        self._frame_id=self.canvas.create_window(0, 0, window=self.frame, anchor='nw')
        self.canvas.pack(side='left', fill='both', expand=True)
        self.canvas.bind("<Configure>", self.resize_frame)
        
    def resize_frame(self, e):
        self.canvas.itemconfig(self._frame_id, width=e.width)

    def resize_scrollregion(self, e):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

class ChatFrame(ScrollableFrame):
    def __init__(self, parent, bgc):
        self.bgc=bgc
        super().__init__(parent, bgc)
        self.pack(side="top", fill="both", expand=True)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=1)

    def getLastRow(self):
        return self.frame.grid_size()[1]

    def sendMessage(self, text):
        RoundedCanvas(self.frame, border_radius=5, padding=10, text=text, maxWidth=300, bgc="#2E84F3").grid(row=self.getLastRow(), column=1, columnspan=3, sticky="e", padx=(0,10), pady=5)
    
    def getMessage(self,user,text):
        RoundedCanvas(self.frame, border_radius=5, padding=10, text=text, maxWidth=300, bgc="#252728", color="#fff").grid(row=self.getLastRow(), column=0, columnspan=3, sticky="w", padx=(10,0), pady=5)

class ChatRoom(tk.Frame):
    def __init__(self, parent):
        self.bgc="#161819"
        self.input_bgc="#1D1F20"
        super().__init__(parent, width=400, bg=self.bgc)
        self.chatFrame=ChatFrame(self, self.bgc)
        chatController=tk.Frame(self, height=30, bg=self.bgc)
        chatController.pack(side="bottom", fill="x",padx=10, pady=10, expand=False)
        self.messageEntry=tk.Entry(chatController, highlightthickness=0, insertbackground="#fff")
        self.messageEntry.pack(side="left", fill="both", expand=True, padx=(0,5))
        self.messageEntry.config(fg='#fff', bg=self.input_bgc, selectbackground="#555555", highlightthickness=0, bd=0)
        sendMessage_btn=RadiusButton(chatController, text=">", height=30, width=30, border_radius=4, padding=0, command=self.sendMessage, bgc="#EC6D46", color="#fff")
        sendMessage_btn.pack(side="right", expand=False)

    def sendMessage(self):
        text=self.messageEntry.get()
        if text.replace(' ','') != '':
            self.chatFrame.sendMessage(text)
            cmd=f"message^^%id%^^{text}\0"
            cSocket.send(cmd.encode('utf-8'))
   
class ClientThread(threading.Thread):
    def __init__(self, gameWindow):
        super().__init__()
        self.gameWindow=gameWindow
        self.start()

    def run(self):
        client_msg=cSocket.recv(BUF_SIZE)
        while client_msg:
            data =client_msg.decode('utf-8')
            while data[len(data) - 1] != '\0':
                client_msg=cSocket.recv(BUF_SIZE)
                data += client_msg.decode('utf-8')
            
            data=data.split('^^')
            print(data[2])
            print(f'from: {data[1]}\n------------')
            self.gameWindow.chatRoom.chatFrame.getMessage(data[1], data[2])
            client_msg=cSocket.recv(BUF_SIZE)

def serverConnecting(window):
    window.start_btn["state"]=tk.DISABLED
    serverIP=socket.gethostbyname(window.ipEntry.get())

    try:
        print('Connecting to %s port %s' % (serverIP, PORT))
        cSocket.connect((serverIP, PORT))
    except socket.error as e:
        window.start_btn["state"]=tk.NORMAL
        Dialog(window, 'Socket error', str(e))
        print('Socket error: %s' % str(e))
        return
    except Exception as e:
        window.start_btn["state"]=tk.NORMAL
        print('Other exception: %s' % str(e))
        Dialog(window, 'Other exception', str(e))
        return 
    serverStart(window.accountEntry.get())

def serverStart(name):
    gameWindow=GameWindow(name)
    ClientThread(gameWindow)
    '''
    try:
        while(1):
            msg=str(input())
            print('from: me\n------------')
            cmd=f"message^^%id%^^{msg}\0"
            #sys.getsizeof(msg)
            cSocket.send(cmd.encode('utf-8'))
    except socket.error as e:
        print('Socket error: %s' % str(e))
    except Exception as e:
        print('Other exception: %s' % str(e))
    finally:
        print('Closing connection.')
            # Close the TCP socket
    '''
    #cSocket.close()

cSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
window=LoginWindow("123456")
