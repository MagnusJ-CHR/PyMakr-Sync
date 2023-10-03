from socket import socket
from socket import AF_INET
from socket import SOCK_DGRAM
from sys import exit

server_port = 12000
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(('', server_port))
print("Klar at modtage!")

while True:
    try:
        message, client_address = server_socket.recvfrom(2048)
        modified_message = message. decode()
        server_socket.sendto(modified_message.encode(), client_address)
        if modified_message != "":
            print(modified_message)
            modified_message = ""
    except KeyboardInterrupt:
        print("CTRL-C trykket, abort!")
        server_socket.close()
        exit()