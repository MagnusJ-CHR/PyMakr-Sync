from machine import I2C
from machine import Pin
from time import sleep,sleep_ms
from mpu6050 import MPU6050
import sys
import time
from neopixel import NeoPixel
from machine import ADC

voltage = ADC(Pin(34, Pin.IN),atten=3)
voltage.atten(ADC.ATTN_11DB)
voltage.width(ADC.WIDTH_12BIT)

timeLastToggle = 0 # Definere en variabel vi bruger for at måle tid med

TotalTackles = 0 # Totale mængde tacklinger under session
Tackles = 0 # Tackles variabel er brugt for at tælle mængder tackles op til 5
TackledState = 0 # Er ikke en "riktig" state, men vi bruger denne på samme måde.

#i2c= I2C(0)

#imu = MPU6050(i2c)

n = 12 # Mængder pixel i ring
p = 25 #Pin i NeoPixel
np = NeoPixel(Pin(p, Pin.OUT), n) #Skabe NeoPixel instanse

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
    voltage_val = voltage.read() # Her læser vi spændning på pin 25
    BatteryLevel = voltage_val * (3.2 / 4096)# Her tar vi de 3.2 volt og deler det med 4096 for at få ud den aktuelle spændning på PIN
    BatteryLevel = BatteryLevel * 1.3125 # Bagefter, eftersom dette er taget gennem spænningsdeleren på grund af at den ikke tåler de 4.2 batteriet kan give ud
    # så kan vi finde ud ration på den aktuelle værdi som udgives gennem at ta 4,2(max spænding) delet med vores aktuelle spænning gennem deleren (3.2)
    # På denne måde så får vi ud ratio på 1.3125, som vi ganger vores 3.2 for at få den aktulle nuværende spænding.
    BatteryPercentage = ((BatteryLevel - 3.0) / ( 4.2 - 3.0)) * 100 # Bagefter laver vi lidt hurtig matematik for at kunde måle % ud fra max og minimum
    #spænding på det aktulle batteri. ( 4.2 til 3.0). Så får vi en % som er nogenlunde korrekt.
    print("Batteriprocent er") #Forklarer sig selv
    print(BatteryPercentage)
    if BatteryPercentage > 80: # Hvis batteri er over 80%, lys de fem dioder vi bruger for at vise batteri%.
        NeoPixelBatteryDisplay(0,100,0,7,12)
    if BatteryPercentage < 80 and BatteryPercentage > 60: #Mellem 80 og 60 %, lys 4 dioder.
        NeoPixelBatteryDisplay(0,100,0,7,11)
    if BatteryPercentage > 40 and BatteryPercentage < 60:#Mellem 60 og 40 %, lys 3 dioder.
        NeoPixelBatteryDisplay(100,100,0,7,10)
    if BatteryPercentage > 15 and BatteryPercentage < 40:#Mellem 40 og 15 %, lys 2 dioder.
        NeoPixelBatteryDisplay(100,0,0,7,9)
    if BatteryPercentage > 0 and BatteryPercentage < 15: # Mellem 15 og 0 %, lys alle dioder i rød. ( indikerer at det er tid at lades!)
        NeoPixelBatteryDisplay(100,0,0,7,12)
    if BatteryPercentage < 0: # Hvis man får denne værdi, så er batteriet meget afladet eller har dårlig kontakt. Check udstyr!
        print("Batteri er meget afladet eller har dålig kontakt med stift!")
    
    

while True:
    try:
        #accel = imu.get_values
        displayTackle(100,0,0)
        np.write()
        """if gps.receive_nmea_data():
            np[12] = (0,255,0)"""
        if time.ticks_diff(time.ticks_ms(), timeLastToggle) > 6000 :
            timeLastToggle = time.ticks_ms()
            getBattery()
            
        
        """if accel() > 10000  and  TackledState == 0:
            TackledState = 1
            Tackles = Tackles + 1
            TotalTackles = TotalTackles + 1
        if accel() in range(-9999,9999):
            TackledState = 0
        if accel() < -10000 and TackledState == 0:
            TackledState = 1
            Tackles = Tackles + 1
            TotalTackles = TotalTackles + 1
        if time.ticks_diff(time.ticks_ms(), timeLastToggle) > 1000:
            print("Totale maengde Tackles \n" + str(TotalTackles))
            timeLastToggle = time.ticks_ms()
            if TotalTackles == 5:
                NeoPxClear()
                Tackles = 0
                np[6] = (0,0,255)
            if TotalTackles == 10:
                NeoPxClear()
                Tackles = 0
                np[6] = (0,255,0)
            if TotalTackles == 15:
                NeoPxClear()
                Tackles = 0
                np[6] = (0,255,255)
                """
        
    except KeyboardInterrupt:
        print("Slukker.")
        sys.exit()