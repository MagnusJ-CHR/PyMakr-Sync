import umqtt_robust2 as mqtt #Importerer de libraries vi behøver
import machine, neopixel
import time
import math
from machine import Pin
from machine import PWM
from time import sleep
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
procentR = 0
procentG = 0
procentB = 0


def px012(r, g , b): # definition at tænde lamper 8-11
    for i in range(0,12):
        np[i] = (r, g , b)
        np.write()
        
def procent(flider, rod , g , b):
    procentR = float(flider) * int(rod)
    procentG = float(flider) * int(g)
    procentB = float(flider) * int(b)
    procentR = math.floor(procentR)
    procentG = math.floor(procentG)
    procentB = math.floor(procentB)
    print(procentR,procentG,procentB)
    return(procentR,procentG,procentB)
  
while True:
    try:
        # Indskriv egen kode her:
        if "#" in mqtt.besked and len(mqtt.besked) == 7: # En IF for at bestæmme hvis vi modtager en hex farvekode-værdi
            try:
                rgb_tuple = hex_til_rgb(mqtt.besked)
                print(f"RGB tuple: {rgb_tuple}\n Her kommer farven som ønskes!") #Printer den i RGB
                lcd.putstr("Din farvekode, omvandlet!") #Siger omvandling er færdig
                px012(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2]) #Bruger den omvandlede farvekode for at skifte
                rod = rgb_tuple[0]
            except:
                print("Du har gjort det forkert!")  #Hvis noget er forkert i farvekoden
        if mqtt.besked.isdigit() and len(mqtt.besked) < 4:
            slider = mqtt.besked
            flider = float(slider)
            
        if len(mqtt.besked) != 0: # Her nulstilles indkommende beskeder
            mqtt.besked = ""
            
        mqtt.sync_with_adafruitIO() # igangsæt at sende og modtage data med Adafruit IO             
        #sleep(1) # Udkommentér denne og næste linje for at se visuelt output
        #print(".", end = '') # printer et punktum til shell, uden et enter        
    
    except KeyboardInterrupt: # Stopper programmet når der trykkes Ctrl + c
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()