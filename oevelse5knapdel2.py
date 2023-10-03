from machine import Pin
from time import sleep

led1=Pin(26, Pin.OUT)
pb1=Pin(4, Pin.IN)
while True:
    sleep (0.1)
    print(pb1.value())
    if pb1.value() == 0:
        led1.value(not led1.value())