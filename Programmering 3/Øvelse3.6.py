import umqtt_robust2 as mqtt
import machine, neopixel
import time
from machine import Pin
from machine import PWM
from time import sleep
from gpio_lcd import GpioLcd
lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
                d4_pin=Pin(33), d5_pin=Pin(32),
                  d6_pin=Pin(21), d7_pin=Pin(22),
                    num_lines=4, num_columns=20)

def hex_til_rgb(hex_farve):
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
  
while True:
    try:
        # Indskriv egen kode her:
        if "#" in mqtt.besked and len(mqtt.besked) == 7:
            try:
                rgb_tuple = hex_til_rgb(mqtt.besked)
                print(f"RGB tuple: {rgb_tuple}\n Her kommer farven som ønskes!")
                lcd.putstr("Din farvekode, omvandlet!")
                px012(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])
            except:
                print("Du har gjort det forkert!") 
            
        if len(mqtt.besked) != 0: # Her nulstilles indkommende beskeder
            mqtt.besked = ""
            
        mqtt.sync_with_adafruitIO() # igangsæt at sende og modtage data med Adafruit IO             
        #sleep(1) # Udkommentér denne og næste linje for at se visuelt output
        #print(".", end = '') # printer et punktum til shell, uden et enter        
    
    except KeyboardInterrupt: # Stopper programmet når der trykkes Ctrl + c
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()