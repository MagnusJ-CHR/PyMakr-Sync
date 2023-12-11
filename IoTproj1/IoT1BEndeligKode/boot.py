import sys
from neopixel import NeoPixel
from machine import Pin
from time import sleep
from machine import ADC
from time import sleep_ms
sys.path.reverse()
print("\n\n\nESP32 starter op")



n = 12 # number of pixels in the Neopixel ring
p = 25 # pin atached to Neopixel ring
np = NeoPixel(Pin(p, Pin.OUT), n) # create NeoPixel instance

def set_color(r, g, b):
    for p in range(n):
        np[p]=(r, g, b)
        np.write()
        sleep(1)

#set_color(100, 0, 0)
    