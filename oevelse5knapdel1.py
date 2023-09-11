from machine import Pin
from time import sleep

led=Pin(26, Pin.OUT)
pb1=Pin(4, Pin.IN)

while True:
    print("Værdi af knap",pb1.value())
    sleep(0.2)

    