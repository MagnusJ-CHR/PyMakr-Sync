from neopixel import NeoPixel
from machine import Pin
from time import sleep, sleep_ms
n = 12 # Mængder pixel i ring
p = 26 #Pin i NeoPixel
np = NeoPixel(Pin(p, Pin.OUT), n) #Skabe NeoPixel instanse
wait = 1000

def clear(): #For at rense al farve i alle pixel
    for i in range(n):
        np[i] = (0, 0 , 0)
        np.write()
        
def fade_in_out(color, wait):
 for i in range(0, 4 * 256, 8):
     for j in range(n):
         if (i // 256) % 2 == 0:
             val = i & 0xff
         else:
             val = 255 - (i & 0xff)
     
     if color == 'red':
         np[j] = (val, 0, 0)
     elif color == 'green': 
         np[j] = (0, val, 0)
     elif color == 'blue':
         np[j] = (0, 0, val)
     elif color == 'purple':
         np[j] = (val, 0, val)
     elif color == 'yellow':
         np[j] = (val, val, 0)
     elif color == 'teal':
         np[j] = (0, val, val)
     elif color == 'white':
         np[j] = (val, val, val)
     np.write()
sleep_ms(wait)
         
fade_in_out('red', 8000)
fade_in_out('green', 20)
fade_in_out('blue', 500)
fade_in_out('purple', 600)
fade_in_out('yellow', 800)
fade_in_out('teal', 900)
fade_in_out('white', 1000)
         
