"""from machine import Pin
from time import sleep
pb1 = Pin(4, Pin.IN)
led1 = Pin(26, Pin.OUT)

while True:
    first = pb1.value()
    sleep(0.01)
    second = pb1.value()
    #tjekker om knap trykkes
    #hvis knap værdi går fra 1 til 0
    if first == 1 and second == 0: # Her tjekker den hvis det er blevet tændt (Starter med nedtrykt og går tilbage til sin gamle værdi)
        print("Knap trykket")
        sleep (0.1)
    if pb1.value() == 0: #Hvis knap er nedtrykt, lav i princip hele øvelse 5 del 2
        led1.value(not led1.value())
        #tjekker om knap slippes
        #hvis knap værdi går fra  0 (false) til (True)
    elif first == 0 and second == 1:
            print("Knap sluppet og")

    """  #Første forsøg på dette, men havde problem med at led forblev på når den ikke sku.
#Fandt meget nemmere version i dette:

from machine import Pin
from time import sleep
pb1 = Pin(4, Pin.IN)
led1 = Pin(26, Pin.OUT)

while True:
    first = pb1.value()
    sleep(0.01)
    second = pb1.value()
    #tjekker om knap trykkes
    #hvis knap værdi går fra 1 til 0
    if first == 1 and second == 0: # Her tjekker den hvis det er blevet tændt (Starter med nedtrykt og går tilbage til sin gamle værdi)
        print("Knap trykket")
        led1.value(not led1.value()) # Gennem at bare sætte denne lille bid kode, laver det ikke problem med extra sleeps osv eftersom denne funktion allerede checker hvis den er på eller ikke!
        #tjekker om knap slippes
        #hvis knap værdi går fra  0 (false) til (True)
    elif first == 0 and second == 1:
            print("Knap sluppet")