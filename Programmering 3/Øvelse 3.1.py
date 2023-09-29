#3.1
from neopixel import NeoPixel #Importerer de libraries vi behøver
from machine import Pin
from time import sleep
n = 12 # Mængder pixel i ring
p = 26 #Pin i NeoPixel
np = NeoPixel(Pin(p, Pin.OUT), n) #Skabe NeoPixel instanse

def clear(): # Definere en funktion at slukke alle lamper
    for i in range(n):
        np[i] = (0, 0 , 0)
        np.write()
        
def px02(r, g , b): # definition at tænde lamper 0-2
    for i in range(0,3):
        np[i] = (r, g , b)
        np.write()

def px36(r, g , b): # definition at tænde lamper 3-5
    for i in range(3,6):
        np[i] = (r, g , b)
        np.write()
        
def px68(r, g , b): # definition at tænde lamper 6-8
    for i in range(6,8):
        np[i] = (r, g , b)
        np.write()
        
def px811(r, g , b): # definition at tænde lamper 8-11
    for i in range(8,11):
        np[i] = (r, g , b)
        np.write() 
    
px02(0,155,0) # tænder 0-2 i korrekt farve
px36(0,0,155) # tænder 3-6 i korrekt farve
px68(155,0,155) # tænder 6-8 i korrekt farve
px811(155,155,0) # tænder 9-11 i korrekt farve
sleep(2)
clear() # For at bli av med det blindende lys!
