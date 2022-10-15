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
        while client_msg:
            data  = client_msg.decode('utf-8')
            while data[len(data) - 1] != '\0':
                client_msg = self.cSocket.recv(BUF_SIZE)
                data += client_msg.decode('utf-8')
            
            data = data.split('^^')
            print(data[2])
            print(f'from: {data[1]}\n------------')
            client_msg = self.cSocket.recv(BUF_SIZE)

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
    try:
        while(1):
            msg = str(input(""))
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

# end of main


if __name__ == '__main__':
	main()
