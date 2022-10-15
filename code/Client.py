####################################################
#  Network Programming - Unit 2 Simple TCP Client Server Program         
#  Program Name: 3-TCPClient.py                                      			
#  The program is a simple TCP client.            		
#  2021.07.13                                                   									
####################################################
import sys
import socket
import threading

PORT = 6666
BUF_SIZE = 1024			# Receive buffer size


class ClientThread(threading.Thread):
    def __init__(self, cSocket):
        super().__init__()
        self.cSocket = cSocket
        self.start()

    def run(self):
        client_msg = self.cSocket.recv(BUF_SIZE)
        print(client_msg.decode('utf-8'))

def main():
	# Get server IP
	# serverIP = socket.gethostbyname(sys.argv[1])
    serverIP = socket.gethostbyname('127.0.0.1')
	
	# Create a TCP client socket
    cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to server
    print('Connecting to %s port %s' % (serverIP, PORT))
    cSocket.connect((serverIP, PORT))
    ClientThread(cSocket)
    # Send message to server
    while(1):
        try:
            msg = str(input("message:"))
            cmd = f"message,1,{sys.getsizeof(msg)},{msg}\0"
            cSocket.send(cmd.encode('utf-8'))
            
        except socket.error as e:
            print('Socket error: %s' % str(e))
        except Exception as e:
            print('Other exception: %s' % str(e))
        finally:
            print('Closing connection.')
    		# Close the TCP socket
    		#cSocket.close()

# end of main


if __name__ == '__main__':
	main()
