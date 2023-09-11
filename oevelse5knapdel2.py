from machine import Pin
from time import sleep

led1=Pin(26, Pin.OUT)
pb1=Pin(4, Pin.IN)
while True:
    sleep (0.1)
    print(pb1.value())
    if pb1.value() == 0:
        led1.value(not led1.value())
 """Denne kode fungerer gennem at spørge hvis PB1 value er 0 eller 1.
 Hvis PB1 er 0 (false) så bliver LED's value sit modsatte. Det betyder at hver gang knappen slukkes (0)
 så bliver faktiskt LED modsat af dens status den var inden. AKA en toggle! Sleep er behøvet ellers modtager
 den for mange kommandoer og blinker."""