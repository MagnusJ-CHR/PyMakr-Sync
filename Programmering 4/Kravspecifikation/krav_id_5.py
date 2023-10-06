from socket import socket
from socket import AF_INET
from socket import SOCK_DGRAM
from sys import exit
from time import sleep_ms
number = 0
pb1 = Pin(4, Pin.IN)
server_port = 12000
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(('', server_port))
print("Klar at modtage!")

while True:
    try:
        message, client_address = server_socket.recvfrom(2048)
        modified_message = message. decode()
        server_socket.sendto(modified_message.encode(), client_address)
        if number == 0 and pb1.value() == 0:
            number = 1
            sleep_ms(200)
        if number == 1 and pb1.value() == 0:
            number = 0 
            sleep_ms(200)
        if modified_message != "" and number == 0:
            print(modified_message)
            modified_message = ""
        if number == 1 and pb1.value() == 1:
            print("Lige nu modtager vi ikke beskeder. Prøv igen senere.")

    except KeyboardInterrupt:
        print("CTRL-C trykket, abort!")
        server_socket.close()
        exit()