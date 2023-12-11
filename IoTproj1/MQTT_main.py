import time
import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

print(IPAddr)

serverName = '10.136.138.172'

serverPort = 12000

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

start_input = input("Tryk for at starte timeren")

start_tid = time.time()


while True:
    _input = input("Noter spillerens nummer og observation")
    slut_tid= time.time()
    timer = int(slut_tid - start_tid)
    minutter = timer // 60
    sekunder = timer % 60
    file = open("Data.txt", "a")
    data = (f"\n{_input} {minutter}m : {sekunder}s Observant: {IPAddr}")
    file.write(data)
    file.close()
    clientSocket.sendto(data.encode(), (serverName, serverPort))
