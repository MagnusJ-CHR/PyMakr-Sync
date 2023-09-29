from machine import Pin, ADC
from time import sleep_ms,sleep
from neopixel import NeoPixel #Importerer de libraries vi behøver
# initialiserer ADC objekt på på pin 34
pot = ADC(Pin(34, Pin.IN),atten=3) # atten 3 = 11dB attenuation (150mV - 2450mV)
pot.atten(ADC.ATTN_11DB) # 11dB attenuation (150mV - 2450mV)
pot.width(ADC.WIDTH_9BIT) # bestemmer opløsningen i bits 12 (111111111111 = 4096)
led1 = Pin(26, Pin.OUT, value=0) # Laver instans af Pin objekt til at styre ledl
"""Del 3, ADC.WIDTH_9BIT Bestæmmer hvor mange bit vi kan bruge til vores værdi.
Så på 9 bit, har vi op til 512, 10 bit 1024, 11bit 2048 og 12bit 4096. Så beroende
på hvor hurtigt eller hvor store værdier man ska bruge, bestæmmer man med den kommando.
(Op til 4096.)"""
n = 13 # Mængder pixel i ring
p = 26 #Pin i NeoPixel
np = NeoPixel(Pin(p, Pin.OUT), n) #Skabe NeoPixel instanse
tal1 = 0
tal2 = 1

def clear(): # Definere en funktion at slukke alle lamper
    for i in range(n):
        np[i] = (0, 0 , 0)
        np.write()
        
def px012(r, g , b): # definition at tænde lamper 0-12
    for i in range(tal1,tal2):
        np[i] = (r, g , b)
        np.write()
        sleep_ms(pot_val)
        
while True: # starter uendeligt while loop
    pot_val = pot.read() # Gemmer aflæsningen af ADC objektets read metode i variablen pot_val
    spaending = pot_val * (3.3 / 4096) # Udregner spændingen og gemmer i variabel
    print("Analog potentiometer vaerdi: ", pot_val) # printer 12Bit ADC værdien
    print("InAnalog potentiometer spaending: ", spaending) #printer spændingen på GPIO 34
    led1.value(not led1.value()) # blinkeer LED
    # kalder sleep_ms funktionen og giver pot_val variablen som argument
    # (for at justere tiden med potmeter)
    px012(100,0,0)
    clear()
    if tal2 < 13:
        tal1 = tal1 + 1
        tal2 = tal2 + 1
    if tal2 == 13:
        tal1 = 11
        tal2 = 12
        sleep_ms(1)
        tal1 = 0
        tal2 = 1
print(tal1,tal2)