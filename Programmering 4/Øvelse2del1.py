from machine import Pin, ADC
from time import sleep_ms,sleep
from neopixel import NeoPixel #Importerer de libraries vi behøver
# initialiserer ADC objekt på på pin 34
pot = ADC(Pin(34, Pin.IN),atten=3) # atten 3 = 11dB attenuation (150mV - 2450mV)
pot.atten(ADC.ATTN_11DB) # 11dB attenuation (150mV - 2450mV)
pot.width(ADC.WIDTH_12BIT) # bestemmer opløsningen i bits 12 (111111111111 = 4096)
led1 = Pin(26, Pin.OUT, value=0) # Laver instans af Pin objekt til at styre ledl

n = 12 # Mængder pixel i ring
p = 26 #Pin i NeoPixel
np = NeoPixel(Pin(p, Pin.OUT), n) #Skabe NeoPixel instanse
def clear(): # Definere en funktion at slukke alle lamper
    for i in range(n):
        np[i] = (0, 0 , 0)
        np.write()
        
def px012(r, g , b): # definition at tænde lamper 0-12
    for i in range(0,12):
        np[i] = (r, g , b)
        np.write()
        
while True: # starter uendeligt while loop
    pot_val = pot.read() # Gemmer aflæsningen af ADC objektets read metode i variablen pot_val
    spaending = pot_val * (3.3 / 4096) # Udregner spændingen og gemmer i variabel
    print("Analog potentiometer vaerdi: ", pot_val) # printer 12Bit ADC værdien
    print("InAnalog potentiometer spaending: ", spaending) #printer spændingen på GPIO 34
    led1.value(not led1.value()) # blinkeer LED
    # kalder sleep_ms funktionen og giver pot_val variablen som argument
    # (for at justere tiden med potmeter)
    sleep_ms(500)
    if pot_val < 500:
        px012(55,0,0)
        sleep_ms(100)
    elif 1500 <= pot_val <= 3000:
        px012(40,30,0)
        sleep_ms(100)
        clear()
        
    elif pot_val > 3000:
        px012(0,55,0)
        sleep_ms(100)