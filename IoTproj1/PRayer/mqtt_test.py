from machine import I2C
from machine import Pin
from machine import UART
from gps_bare_minimum import GPS_Minimum
from time import sleep,sleep_ms
from mpu6050 import MPU6050
import sys
import time
from neopixel import NeoPixel
from machine import ADC
import umqtt_robust2 as mqtt
import _thread
from math import radians, cos, sin, asin, sqrt


# CONFIGURATION
gps_port = 2                               # ESP32 UART port, Educaboard ESP32 default UART port
gps_speed = 9600                           # UART speed, defauls u-blox speed
uart = UART(gps_port, gps_speed)           # UART object creation
gps = GPS_Minimum(uart)                    # GPS object creation
###########################################################################################################################################
# Tidsvariabler for time.ticks
timeLastToggle = 0 						   # Definere en variabel vi bruger for at måle tid med
timeLastToggleGPS = 0					   # Definere en variabel vi bruger for at måle tid med, til brug af GPS:en
###########################################################################################################################################
#Til brug i vores "condition"
Stage = 0						   # Definerer en variabel, som vi bruger som en condition.
###########################################################################################################################################
#Til brug i at regne ud totale mængde meter spillere har rørt sig under kampen.
TotalM = 0 								   # Definerer en variabel, som vi bruger for at lagre Totale mængde meter under kampen
###########################################################################################################################################
#Til brug at måle mængde tacklinger
TotalTackles = 0 						   # Totale mængde tacklinger under session
Tackles = 0 						   	   # Tackles variabel er brugt for at tælle mængder tackles op til 5
TackledState = 0 						   # Er ikke en "riktig" state, men vi bruger denne på samme måde.
###########################################################################################################################################
#Til brug i NeoPixel
n = 12 									   # Mængder pixel i ring
p = 32 									   #Pin i NeoPixel
np = NeoPixel(Pin(p, Pin.OUT), n) 		   #Skabe NeoPixel instanse
###########################################################################################################################################
#I2C
i2c= I2C(0) 							   # Brugt for at åbne I2C port 0, så vi kan bruge den
imu = MPU6050(i2c) 						   # Laver om en variabel til at være modsvarende det vi læser fra vores MPU modul.
###########################################################################################################################################
#Til at åbne vores GPIO34 for at kunde avlæse batterispændingsdeler
voltage = ADC(Pin(34))					   # Laver en variabel til værdien af pin 34
voltage.atten(ADC.ATTN_11DB) 			   # Attenuering af værdi
voltage.width(ADC.WIDTH_12BIT)             # Størrelse på data i bits.
###########################################################################################################################################
# Hvordan vi viser vores Tacklinger på NeoPixel
def displayTackle(r, g , b): 			   # Definerer en funktion for at ændre farver på Neopixel ring beroende på "Tackles" værdi.
    if Tackles in range(1,6):              # Hvis tacklinger er indenfor 1-6,
        np[Tackles] = (r, g , b)		   # Lav om mængde tildelte lysdioder til mængden tacklinger ( op til 5)
        np.write()						   # Tænd lysdioder som har fået tildelet sin farve
###########################################################################################################################################
# For at tænde alle NeoPixels
def NeoPixelEnableAll(r , g , b): 		   # Definerer en funktion for at tænde alle NeoPixel dioder.
    for i in range(0,12):
        np[i] = (r ,g , b)
        np.write()
###########################################################################################################################################
# NeoPixel funktion for at vise batterikapacitet
def NeoPixelAnyRange(r , g , b , RangeValue1,RangeValue2): # Her laver vi en funktion for at kunde bestæmme begge farve og vilke
    for i in range(RangeValue1,RangeValue2):					 # lysdioder som skal tændes, så vi ikke behøver en ny funktion hver gang.	
        np[i] = (r ,g , b)
        np.write()
###########################################################################################################################################
# For at rense alle lysdioder
def NeoPixelClear(): 					   #Som navnet på funktionen siger, den "renser" alle lysdioder ned til 0. AKA de er slukket.
    for i in range(0,12):
        np[i] = (0,0,0)
        np.write()
###########################################################################################################################################
# For at enbart rense dioder på siden af batteri kapacitetmåler.
def NeoPixelClearBatt(): 				   # Den "renser" lysdioder ned til 0. AKA de er slukket.
    for i in range(7,12): 				   # MEN kun under alle lysdioder vores batteri% viser bruger!
        np[i] = (0,0,0)
        np.write()
###########################################################################################################################################'
# For at hemte batteristatus.
def getBattery():
    voltage_val = voltage.read()              
    BatteryLevel = voltage_val * (3.2 / 4096) 
    BatteryLevel = BatteryLevel * 1.3125     
    # En funktion for at hæmte batteri status og avsende data til Dashboard
    # Læser spænding på pin 34 fra batterispændingsdeler
    # Her tar vi de 3.2 volt og deler det med 4096 for at få ud den aktuelle spændning på PIN
    # Bagefter, eftersom dette er taget gennem Batterispændingsdeler
    # så kan vi finde ud ration på den aktuelle værdi som udgives gennem at ta 4,2(max spænding) delet med vores aktuelle spænning gennem deleren (3.2)
    BatteryPercentage = (BatteryLevel / 4.2) * 100 #Her regner vi ud % af Batteriet tilbage på batteriet.
    print("Batteriprocent er")
    print(BatteryPercentage) # Seperate prints for at MicroPython ikke syndes om at lave om en float til string.
    if BatteryPercentage > 80: # Hvis batteri er over 80%, lys de fem dioder vi bruger for at vise batteri%.
        NeoPixelClearBatt()
        NeoPixelAnyRange(0,255,0,7,12)
    elif BatteryPercentage < 80 and BatteryPercentage > 60:  #Mellem 80 og 60 %, lys 4 dioder.
        NeoPixelClearBatt()
        NeoPixelAnyRange(0,255,0,7,11)
    elif BatteryPercentage > 40 and BatteryPercentage < 60: #Mellem 60 og 40 %, lys 3 dioder.
        NeoPixelClearBatt()
        NeoPixelAnyRange(255,255,0,7,10)
    elif BatteryPercentage > 20 and BatteryPercentage < 40: #Mellem 40 og 15 %, lys 2 dioder.
        NeoPixelClearBatt()
        NeoPixelAnyRange(255,0,0,7,9)
    elif BatteryPercentage > 0 and BatteryPercentage < 20: # Mellem 15 og 0 %, lys alle dioder i rød. ( indikerer at det er tid at lades!)
        NeoPixelClearBatt()
        NeoPixelAnyRange(255,0,0,7,12)
    elif BatteryPercentage < 0: # Hvis man får denne værdi, så er batteriet meget afladet eller har dårlig kontakt. Check udstyr!
        NeoPixelClearBatt()
        print("Batteri er meget afladet eller har dålig kontakt med stift!")
    return BatteryPercentage
#################################################################################################################################
#Funktion for at modtage korrekt data fra GPS data og returne det for at afsende til Adafruit
def gps_ticks():
    speed = lat = lon = None 							 # laver om speed, lat og lon til en null value
    if gps.receive_nmea_data():							 # Hvis vi modtager data fra GPS 
        if gps.get_speed() != -999 and gps.get_latitude() != -999.0 and gps.get_longitude() != -999.0 and gps.get_validity() == "A":
            # Hvis denne data har kommet fra en satellit =/ Den er gyldig, lav om de tre variabler til de værdier modtaget
            speed = str(gps.get_speed())
            lat = str(gps.get_latitude())
            lon = str(gps.get_longitude())
            return speed + "," + lat + "," + lon + "," + "0.0" # Returner dem i deres korrekte type
        else:
            print("Savner opkobling mod satellit!") 	 # Hvis den data ikke er gyldig.
            return False
    else:
        return False
#################################################################################################################################
# Nokk den ondeste koden i hele dette .py projekt. # Matematikfunktion for at beregne distance fra to forskellige koordinater i meter 
def haversine(lon1, lat1, lon2, lat2): 					 
    TotalMeters = 0
    Meters = 0
    # konverter decimal grader til radianer
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # Vi kan regne ud buelængde gennem (buelængde = vinkel i radianer * radius)
    # Jeg har meget svært med at forstå formulaen. Kig her for forklaring.
    dlon = lon2 - lon1 
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 										# Radianse af jorden i kilometer.
    DistanceKM = c * r
    Meters = DistanceKM * 1000 						# Omvandler vi kilometer til meter
    TotalMeters = TotalMeters + Meters
    if Meters > 1000: 							# Første opstart har en bug med at den første måling altid
        return False       							# bliver under -30000k. Denne kode fixer det med at melde den som false. Der er nok heller ikke nogen som løber 1000m på 8 sekunder
    else:
        if TotalMeters > 1000 and TotalMeters < 2000:
            np[0] = (100,0,0)
            np.write()
        elif TotalMeters > 2000 and TotalMeters < 3000: # Her checker vi værdien af TotalMeter for at vise mængde meter løbet under session, vist i farve. Dette viser vi i lysiode 0.
            np[0] = (0,100,0)
            np.write()
        elif TotalMeters > 3000 and TotalMeters < 4000:
            np[0] = (0,0,100)
            np.write()
        elif TotalMeters > 4000:
            np[0] = (100,100,100)
            np.write()
        return TotalMeters
    


# Her kan i placere globale varibaler, og instanser af klasser
NeoPixelClear() # Tar vek gammel lysdiode farve, i opstarten af program

while True:
    try:
        # Indskriv egen kode her:
        accelerometer = imu.get_values #Laver en variabel med værdierne fra IMU accelerometererometer
        displayTackle(100,0,0) # Start funktion
        # Denne kode under, kunde være en funktion. Men uandset vad som en prøvedes, så vil den ikke fungere under sin egen def().
        if accelerometer() > 15000  and  TackledState == 0: # Her bruger vi de værdier vi har defineret tidligare for at lave en form af "state".
            TackledState = 1 								# State blir 1
            Tackles = Tackles + 1 							# Vi inkrementerer Tacklinger med 1
            TotalTackles = TotalTackles + 1 				# Og vi inkrementerer den totale mængde tacklinger med et.
        if accelerometer() in range(-7000,7000):
            TackledState = 0 								# Hvis spillere har stilt sig op, lav state om til 0
        if accelerometer() < -15000 and TackledState == 0:  # Kig kommentar under accelerometer() > 10000
            TackledState = 1
            Tackles = Tackles + 1
            TotalTackles = TotalTackles + 1
        if TotalTackles == 5: 								#Vis mængde tacklinger er 5 , start om Tackles til 0 og vis en blå diode for at betyde "5".
                NeoPixelClear()
                Tackles = 0
                np[6] = (0,0,255)
        elif TotalTackles == 10:								#Vis mængde tacklinger er 10 , start om Tackles til 0 og vis en Grøn diode for at betyde "5".
                NeoPixelClear()
                Tackles = 0
                np[6] = (0,255,0)
        elif TotalTackles == 15:								#Vis mængde tacklinger er 15 , start om Tackles til 0 og vis en Gul diode for at betyde "5".
                NeoPixelClear()
                Tackles = 0
                np[6] = (255,0,255)
            
        
        if time.ticks_diff(time.ticks_ms(), timeLastToggleGPS) > 4000: # Hver 4 sekunder, eksekver kode.
            Stage = Stage + 1										   # Her bruger vi vores variabel vi tildelte 0 tidligere , som inkrementerer med 1 hver 4 sek.
            timeLastToggleGPS = time.ticks_ms()						   # Her laver vi om timeLastToggleGPS til time.ticks_ms . Derfor kan den se diff hver fire sek.											
            if Stage == 1: 										  	   # Her har vi vores første stage, af de to den alternerer mellem.
                mqtt.web_print(getBattery())						   # Hemter batteri % og afsender til Adafruit.io Dashboard
                lat1 = gps.get_latitude()							   # Hemter første set af koordinater
                lon1 = gps.get_longitude()							   # ^

            if Stage == 2:											   # Stage 2
                gps_ticks()											   # Eksekver gps_ticks() funktion
                mqtt.web_print(gps_ticks(), 'oqoqo/feeds/iotmap1/csv') # Afsend al data om nuvarende pos til Adafruit.io Dashboard
                Stage = 0											   # Lav om stage til 0, så det looper uendligt
                lat2 = gps.get_latitude()							   # Hemt andre set af koordinater
                lon2 = gps.get_longitude()							   # ^
                TotalM = haversine(lon1, lat1, lon2, lat2) + TotalM    # Her laver vi variabeln som tæller sammen totale mængde meter under nuvarende session.
                print("Total mængde meter rørt sig.")                  #
                print(TotalM)										   #Her printer vi ud alle de relevante data vi vil have udprintet, så vi ved dem.
                print("Forventede hastighed")						   #
                print(gps.get_speed())								   # + Hastighed, hvorfor ikke?
            # difference på 120000 ( 2 min ) mellem timeLastToggle værdi og den der teller ticks (time.ticks_ms), eksekver.
        
            
        if len(mqtt.besked) != 0: # Her nulstilles indkommende beskeder
            mqtt.besked = ""
            
        mqtt.sync_with_adafruitIO() # igangsæt at sende og modtage data med Adafruit IO                  
    
    except KeyboardInterrupt: # Stopper programmet når der trykkes Ctrl + c
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()