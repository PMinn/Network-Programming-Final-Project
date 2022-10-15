####################################################
#  Network Programming - Unit 2 Simple TCP Client Server Program         
#  Program Name: 3-TCPServer.py                                      			
#  The program is a simple TCP server.            		
#  2021.07.13                                                   									
####################################################
import socket

PORT = 6001
backlog = 5
BUF_SIZE = 1024			# Receive buffer size

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
	print('Waiting to receive message from client')
	client, (rip, rport) = srvSocket.accept()
	
	# Receive client message, buffer size = BUF_SIZE
	client_cmd = client.recv(BUF_SIZE)
	if client_cmd:
		cmd = client_cmd.decode('utf-8').split(',')
		# msg = "from IP: " + str(rip) + " port: " + str(rport)
		client.send('111'.encode('utf-8'))
		sizeOfMsg = int(cmd[2])
		print(f'size:{sizeOfMsg}')
		client_msg = client.recv(sizeOfMsg)
		if client_msg:
			print(client_msg.decode('utf-8'))
	client.close()
	srvSocket.close()
# end of main

if __name__ == '__main__':
	main()
