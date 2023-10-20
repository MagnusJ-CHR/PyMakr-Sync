from machine import I2C
from machine import Pin
from time import sleep,sleep_ms
from mpu6050 import MPU6050
import sys
import time
from neopixel import NeoPixel
from machine import ADC
import umqtt_robust2 as mqtt

n = 12 # Mængder pixel i ring
p = 25 #Pin i NeoPixel
np = NeoPixel(Pin(p, Pin.OUT), n) #Skabe NeoPixel instanse

voltage = ADC(Pin(34))
voltage.atten(ADC.ATTN_11DB)
voltage.width(ADC.WIDTH_12BIT)

def displayTackle(r, g , b): # Definerer en funktion for at ændre farver på Neopixel ring beroende på "Tackles" værdi.
    if Tackles in range(1,6):
        np[Tackles] = (r, g , b)
        np.write()

def NeoPixelEnableAll(r , g , b): # Definerer en funktion for at tænde alle NeoPixel dioder.
    for i in range(0,12):
        np[i] = (r ,g , b)
        np.write()
        
def NeoPixelBatteryDisplay(r , g , b , RangeValue1,RangeValue2): # Her laver jeg en funktion for at kunde bestæmme begge farve og vilke
    for i in range(RangeValue1,RangeValue2):					#lysdioder som skal tændes, så jeg ikke behøver en ny funktion hver gang.	
        np[i] = (r ,g , b)
        np.write()
        
def NeoPixelClear(): #Som navnet på funktionen siger, den "renser" alle lysdioder ned til 0. AKA de er slukket.
    for i in range(0,12):
        np[i] = (0,0,0)
        np.write()

def getBattery():
    voltage_val = voltage.read()
    BatteryLevel = voltage_val * (3.2 / 4096)
    BatteryLevel = BatteryLevel * 1.3125
    BatteryPercentage = ((BatteryLevel - 3.0) / ( 4.2 - 3.0)) * 100
    print("Batteriprocent er")
    print(BatteryPercentage)
    mqtt.web_print(BatteryPercentage)
    if BatteryPercentage > 80:
        NeoPixelBatteryDisplay(0,255,0,7,12)
        mqtt.web_print(BatteryPercentage)
    if BatteryPercentage < 80 and BatteryPercentage > 60: 
        NeoPixelBatteryDisplay(0,255,0,7,11)
    if BatteryPercentage > 40 and BatteryPercentage < 60:
        NeoPixelBatteryDisplay(255,255,0,7,10)
    if BatteryPercentage > 20 and BatteryPercentage < 40:
        NeoPixelBatteryDisplay(255,0,0,7,9)
    if BatteryPercentage > 0 and BatteryPercentage < 20:
        NeoPixelBatteryDisplay(255,0,0,7,12)
    if BatteryPercentage < 0:
        print("Batteri er meget afladet eller har dålig kontakt med stift!")



timeLastToggle = 0 # Definere en variabel vi bruger for at måle tid med


# Her kan i placere globale varibaler, og instanser af klasser

while True:
    try:
        # Indskriv egen kode her:
        if time.ticks_diff(time.ticks_ms(), timeLastToggle) > 120000 :
            timeLastToggle = time.ticks_ms()
            getBattery()
            
        if len(mqtt.besked) != 0: # Her nulstilles indkommende beskeder
            mqtt.besked = ""
            
        mqtt.sync_with_adafruitIO() # igangsæt at sende og modtage data med Adafruit IO             
        #sleep(1) # Udkommentér denne og næste linje for at se visuelt output
        #print(".", end = '') # printer et punktum til shell, uden et enter        
    
    except KeyboardInterrupt: # Stopper programmet når der trykkes Ctrl + c
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()