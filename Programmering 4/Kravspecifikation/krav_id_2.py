from neopixel import NeoPixel #Importerer de libraries vi behøver
# initialiserer ADC objekt på på pin 34
from machine import Pin
from time import sleep_ms,sleep
n = 13 # Mængder pixel i ring
p = 26 #Pin i NeoPixel
np = NeoPixel(Pin(p, Pin.OUT), n) #Skabe NeoPixel instanse
tal1 = 0
tal2 = 1
tal3 = 0
tal4 = 1
pb1=Pin(4, Pin.IN)

def clear(): # Definere en funktion at slukke alle lamper
    for i in range(n):
        np[i] = (0, 0 , 0)
        np.write()
        
def pxhop(r, g , b): # definition at tænde lamper 0-12
    for i in range(tal1,tal2):
        np[i] = (r, g , b)
        np.write()
        pxhopminus(0,0,0)
        sleep_ms(200)
        
def pxhopminus(r,g,b):
    for i in range(tal3,tal4):
        np[i] = (r, g , b)
        np.write()
        sleep_ms(40)
        
while True: # starter uendeligt while loop
        if pb1.value() == 0:
            pxhop(100,0,0)
            if tal2 < 13:
                tal1 = tal1 + 1
                tal2 = tal2 + 1
                tal3 = tal1 - 1
                tal4 = tal2 - 1
                print(tal1,tal2)
                print(tal3,tal4)
            if tal2 == 13:
                tal1 = 11
                tal2 = 12
                sleep_ms(5)
                tal1 = 0
                tal2 = 1
                print(tal1,tal2)
            