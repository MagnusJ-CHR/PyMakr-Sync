from machine import Pin
from time import sleep

led=Pin(26, Pin.OUT)
pb1=Pin(4, Pin.IN)
while True:
    led.value(not pb1.value())
    sleep(0.1)

    