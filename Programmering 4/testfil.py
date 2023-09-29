import machine, neopixel
import time
import math
from machine import Pin
from machine import PWM
from time import sleep_ms,sleep
from gpio_lcd import GpioLcd
lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25), # Definerer vores LCD så den kan bruges.
                d4_pin=Pin(33), d5_pin=Pin(32),
                  d6_pin=Pin(21), d7_pin=Pin(22),
                    num_lines=4, num_columns=20)

def hex_til_rgb(hex_farve): # Funktion for at omstille HEX til RGB farvekode.
    hex_farve = hex_farve.strip('#')
    rgb_liste = []
    for i in range(0, 6, 2):
        rgb_liste.append(int(hex_farve[i:i + 2], 16))
    return tuple(rgb_liste)

# number of pixels
n = 12
# strip control gpio
p = 26
np = neopixel.NeoPixel(machine.Pin(p), n)
# set single pixel (1st pixel = index [0]) to red color
np[0] = (255, 0, 0)
np.write()
time.sleep(1)


def px012(r, g , b): # definition at tænde lamper 8-11
    for i in range(0,12):
        np[i] = (r, g , b)
        np.write()
        
def procent(slider, r , g , b):
    procentR = float(slider) * int(r)
    procentG = float(slider) * int(g)
    procentB = float(slider) * int(b)
    procentR = math.floor(procentR)
    procentG = math.floor(procentG)
    procentB = math.floor(procentB)
    print(procentR,procentG,procentB)
    
while True:
    procent(0.8, 100 , 220 , 110)
    sleep_ms(500)
  
                


