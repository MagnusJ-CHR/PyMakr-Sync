from machine import Pin
from time import sleep


RED_PIN = 26
led1 = Pin(RED_PIN, Pin.OUT)
led1.on()
sleep(0.8)
YLW_PIN = 12
led2 = Pin(YLW_PIN, Pin.OUT) # Samme som tidligere udgaver, her startes alt og kør en lille testrunde.
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
    print("YLW led2 ON!") # Her, istedet for at slukke dem en after hinanden, lader vi bare vær med at slukke tils alle er tændt sammen.
    ... # Samtidigt så har vi så klart ingen Sleep funktion, eftersom så bliver de ud af sync med hinanden.
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