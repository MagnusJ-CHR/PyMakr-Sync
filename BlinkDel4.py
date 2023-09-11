from machine import Pin
from time import sleep


RED_PIN = 26
led1 = Pin(RED_PIN, Pin.OUT)
led1.on()
sleep(0.8)
YLW_PIN = 12
led2 = Pin(YLW_PIN, Pin.OUT)
led2.on()
sleep(0.5)
GRN_PIN = 13
led3 = Pin(GRN_PIN, Pin.OUT)
led3.on()
sleep(0.1)

while True:
    print("Red led1 ON!")
    led1.on()
    print("Red led1 OFF!")
    ...
    print("YLW led2 ON!")
    led2.off()
    print("YLW led2 OFF!")
    ...
    print("GRN led3 ON!")
    led3.on()
    print("GRN led3 OFF!")
    sleep(1)
    led1.off()
    led2.on()
    led3.off()
    sleep(1)