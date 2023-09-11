from machine import Pin
from time import sleep

led1=Pin(26, Pin.OUT)
pb1=Pin(4, Pin.IN)

while True
    print(pb1.value())
    sleep(0.5)