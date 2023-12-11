from socket import socket
from socket import AF_INET
from socket import SOCK_DGRAM
import os
from datetime import datetime, timedelta
 
current_time = datetime.utcnow()
formatted_time = current_time + timedelta(hours=2)
dato = formatted_time.strftime('%Y-%m-%d')
tid = formatted_time.strftime('%H.%M.%S')
datotid = f'{dato} {tid}'
folder_name = f'Observationer ({datotid})'
os.mkdir(folder_name)
file_path = f'./Observationer ({datotid})/'
 
server_port = 12000
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(('', server_port))
print('server is ready to recieve')
while True:
    try:
        message, client_address = server_socket.recvfrom(2048)
        #print(client_address())
        modified_message = message.decode()
        server_socket.sendto(modified_message.encode(), client_address)
        if '##!, ' in modified_message:
            messege = modified_message.split(',')
            if os.path.isfile(file_path + 'Spillernummer ' + messege[1] + '.txt') == False:
                with open(file_path + 'Spillernummer ' + messege[1] + '.txt', "a") as file:
                    file.write(f'Spiller observationer for spiller nummer{messege[1]}\nObservationerne er lavet d. {dato}\n\nObservationerne er formateret som:\nTidspunkt, Afsender, Observation\n\n')
            with open(file_path + 'Spillernummer ' + messege[1] + '.txt', "a") as file:
                file.write(f'*{messege[4]} -{messege[3]}:{messege[2]}\n')
 
        if modified_message != '':
            print(modified_message)
            #print(client_address())
            modified_message = ''
    except KeyboardInterrupt:
        print('CTRL-C pressed, closing down!')
        server_socket.close()
        exit()