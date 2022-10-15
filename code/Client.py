####################################################
#  Network Programming - Unit 2 Simple TCP Client Server Program         
#  Program Name: 3-TCPClient.py                                      			
#  The program is a simple TCP client.            		
#  2021.07.13                                                   									
####################################################
import sys
import socket

PORT = 6666
BUF_SIZE = 1024			# Receive buffer size

def main():
	# Get server IP
	# serverIP = socket.gethostbyname(sys.argv[1])
	serverIP = socket.gethostbyname('127.0.0.1')
	
	# Create a TCP client socket
	cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# Connect to server
	print('Connecting to %s port %s' % (serverIP, PORT))
	cSocket.connect((serverIP, PORT))
	
	# Send message to server
	try:
		msg = "測試11測試11測試11測試11測試11測試11測試11測試11測試11測試11測試11測試11測試11測試11測試11測試11測試11測試1180"
		cmd = f"message,1,{sys.getsizeof(msg)}"
		cSocket.send(cmd.encode('utf-8'))
		client_msg = cSocket.recv(1024)
		cSocket.send(msg.encode('utf-8'))
	except socket.error as e:
		print('Socket error: %s' % str(e))
	except Exception as e:
		print('Other exception: %s' % str(e))
	finally:
		print('Closing connection.')
		# Close the TCP socket
		cSocket.close()

# end of main


if __name__ == '__main__':
	main()
