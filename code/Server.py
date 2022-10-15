####################################################
#  Network Programming - Unit 2 Simple TCP Client Server Program         
#  Program Name: 3-TCPServer.py                                      			
#  The program is a simple TCP server.            		
#  2021.07.13                                                   									
####################################################
import socket
import threading

PORT = 6666
backlog = 5
BUF_SIZE = 1024			# Receive buffer size

class ServerThread(threading.Thread):
    def __init__(self, client_sc, rip, rport):
        super().__init__()
        self.client = client_sc
        self.rip = rip
        self.rport = rport
        print(f"user connect {str(rip)}:{str(rport)}")
        self.start()

    def run(self):
        #name = threading.current_thread().name
        client_msg = self.client.recv(BUF_SIZE)

        while client_msg:
            cmd = client_msg.decode('utf-8').split(',')
            self.client.send('111'.encode('utf-8'))
            sizeOfMsg = int(cmd[2])
            print(f'size:{sizeOfMsg}')
            self.recvMsgContent(sizeOfMsg)
            client_msg = self.client.recv(BUF_SIZE)
        self.client.close()
        
    def recvMsgContent(self, size):
        client_msg = self.client.recv(size)
        print(client_msg.decode('utf-8'))

def main():
	# Create a TCP Server socket
    srvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Enable reuse address/port
    srvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	
	# Bind 	on any incoming interface with PORT, '' is any interface
    print('Starting up server on port: %s' % (PORT))
    srvSocket.bind(('', PORT))
	
	# Listen incomming connection, connection number = backlog (5)
    srvSocket.listen(backlog)
	
	# Accept the incomming connection
    while(1):
        print('Waiting to receive message from client')
        client, (rip, rport) = srvSocket.accept()
        ServerThread(client, rip, rport)
    
    srvSocket.close()
# end of main

if __name__ == '__main__':
	main()
