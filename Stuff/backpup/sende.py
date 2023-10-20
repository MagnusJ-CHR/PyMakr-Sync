import sys,uselect
from machine import UART

uart_remote_port = 1
uart_remote_pin_tx = 33
uart_remote_pin_rx = 32
uart_remote_speed = 9600

group_id = 99

uart_remote = UART(uart_remote_port, baudrate = uart_remote_speed, tx = uart_remote_pin_tx, rx = uart_remote_pin_rx)

usb = uselect.poll()
usb.register(sys.stdin, uselect.POLLIN)

print("To vejs kommunikation")

while True:
    if uart_remote.any() > 0:
        string = uart_remote.read().decode()
        string = string.strip()
        print("REmote: " + string)
    
    if usb.poll(0):
        string = sys.stdin.readline()
        sys.stdin.readline()
        string = string.strip()
        print("USB  : " + string)
        uart_remote.write(string + "\n")
        