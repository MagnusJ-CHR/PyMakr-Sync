from machine import Pin
from time import sleep

pb1 = Pin(4, Pin.IN)
vardi=0
while True:
    if pb1.value() == 0: # Hvis knappen bliver trykket (værdien som knappen viser når den er trykket ned) så lav det under
        vardi = vardi + 1 # Tar værdien af "vardi" og lægger + 1 mens knappen bliver trykket.
        print(vardi) # skriver ud værdien
        sleep(0.5) # Så at den ikke lægger til 300 tal på et knaptryk, så har vi en timer så det lægger til en af gangen hver 0.5s.
        #Har prøvet med 0.1s på sleep, så går det meget stærkt.