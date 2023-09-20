from neopixel import NeoPixel
from machine import Pin
from time import sleep
n = 12 # Mængder pixel i ring
p = 26 #Pin i NeoPixel
np = NeoPixel(Pin(p, Pin.OUT), n) #Skabe NeoPixel instanse

def clear(): #For at rense al farve i alle pixel
    for i in range(n):
        np[i] = (0, 0 , 0)
        np.write()
        
def allpx(r, g , b): # for at angive en pixel værdi alle pixel ska blive
    for i in range(n):
        np[i] = (r, g , b)
        np.write()
while True: #Forevigt loop, lav alle px (allpx funktion) til en svag rød
    allpx(125,0,0) # bagefter, clear alle pixel, sov i en sekund og repeat.
    clear()
    sleep(1)
