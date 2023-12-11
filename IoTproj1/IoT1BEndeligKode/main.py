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
gps_port = 2                              
gps_speed = 9600                           
uart = UART(gps_port, gps_speed)           
gps = GPS_Minimum(uart)                    
###########################################################################################################################################
# Tidsvariabler for time.ticks
timeLastToggle = 0 						   
timeLastToggleGPS = 0					   
###########################################################################################################################################
#Til brug i vores "condition"
Stage = 0						   
###########################################################################################################################################
TotalM = 0 								   
###########################################################################################################################################
#Til brug at måle mængde tacklinger
TotalTackles = 0 						   
Tackles = 0 						   	   
TackledState = 0 						   
###########################################################################################################################################
#Til brug i NeoPixel
n = 12 									   
p = 32 									   
np = NeoPixel(Pin(p, Pin.OUT), n) 		   
###########################################################################################################################################
#I2C
i2c= I2C(0) 							   
imu = MPU6050(i2c) 						   
###########################################################################################################################################
#Til at åbne vores GPIO34 for at kunde avlæse batterispændingsdeler
voltage = ADC(Pin(34))					   
voltage.atten(ADC.ATTN_11DB) 			   
voltage.width(ADC.WIDTH_12BIT)             
###########################################################################################################################################
# Hvordan vi viser vores Tacklinger på NeoPixel
def displayTackle(r, g , b): 			   
    if Tackles in range(1,6):              
        np[Tackles] = (r, g , b)		   
        np.write()						   
###########################################################################################################################################
# For at tænde alle NeoPixels
def NeoPixelEnableAll(r , g , b): 		   
    for i in range(0,12):
        np[i] = (r ,g , b)
        np.write()
###########################################################################################################################################
# NeoPixel funktion for at vise batterikapacitet
def NeoPixelAnyRange(r , g , b , RangeValue1,RangeValue2): 
    for i in range(RangeValue1,RangeValue2):					 
        np[i] = (r ,g , b)
        np.write()
###########################################################################################################################################
# For at rense alle lysdioder
def NeoPixelClear(): 					   
    for i in range(0,12):
        np[i] = (0,0,0)
        np.write()
###########################################################################################################################################
# For at enbart rense dioder på siden af batteri kapacitetmåler.
def NeoPixelClearBatt(): 				   
    for i in range(7,12): 				   
        np[i] = (0,0,0)
        np.write()
###########################################################################################################################################'
# For at hemte batteristatus.
def getBattery():
    voltage_val = voltage.read()               
    BatteryLevel = voltage_val * (3.2 / 4096)
    BatteryLevelTimes = BatteryLevel * 1.9
    print(BatteryLevel)
    print(BatteryLevelTimes)

    BatteryPercentage = (83 * BatteryLevelTimes) - 248 
    print("Batteriprocent er")
    print(BatteryPercentage) 
    if BatteryPercentage > 80: 
        NeoPixelClearBatt()
        NeoPixelAnyRange(0,1,0,7,12)
    elif BatteryPercentage < 80 and BatteryPercentage > 60:  
        NeoPixelClearBatt()
        NeoPixelAnyRange(0,1,0,7,11)
    elif BatteryPercentage > 40 and BatteryPercentage < 60: 
        NeoPixelClearBatt()
        NeoPixelAnyRange(1,1,0,7,10)
    elif BatteryPercentage > 20 and BatteryPercentage < 40: 
        NeoPixelClearBatt()
        NeoPixelAnyRange(1,0,0,7,9)
    elif BatteryPercentage > 0 and BatteryPercentage < 20: 
        NeoPixelClearBatt()
        NeoPixelAnyRange(1,0,0,7,12)
    elif BatteryPercentage < 0: 
        NeoPixelClearBatt()
        print("Batteri er meget afladet eller har dålig kontakt med stift!")
    return BatteryPercentage
#################################################################################################################################
#Funktion for at modtage korrekt data fra GPS data og returne det for at afsende til Adafruit
def gps_ticks():
    speed = lat = lon = None 							
    if gps.receive_nmea_data():							
        if gps.get_speed() != -999 and gps.get_latitude() != -999.0 and gps.get_longitude() != -999.0 and gps.get_validity() == "A":
           
            speed = str(gps.get_speed())
            lat = str(gps.get_latitude())
            lon = str(gps.get_longitude())
            return speed + "," + lat + "," + lon + "," + "0.0" 
        else:
            print("Savner opkobling mod satellit!") 	 
            return False
    else:
        return False
#################################################################################################################################
def haversine(lon1, lat1, lon2, lat2): 					 
    TotalMeters = 0
    Meters = 0
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
   
    dlon = lon2 - lon1 
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 										
    DistanceKM = c * r
    Meters = DistanceKM * 1000 						
    TotalMeters = TotalMeters + Meters
    if Meters > 1000: 							
        return False       							
    else:
        return TotalMeters
    



NeoPixelClear() 

while True:
    try:
        accelerometer = imu.get_values 
        displayTackle(1,0,0) 
        
        if accelerometer() > 15000  and  TackledState == 0: 
            TackledState = 1 								
            Tackles = Tackles + 1 							
            TotalTackles = TotalTackles + 1 				
        if accelerometer() in range(-7000,7000):
            TackledState = 0 								
        if accelerometer() < -15000 and TackledState == 0:  
            TackledState = 1
            Tackles = Tackles + 1
            TotalTackles = TotalTackles + 1
        if TotalTackles == 5: 								
                NeoPixelClear()
                Tackles = 0
                np[6] = (0,0,1)
        elif TotalTackles == 10:								
                NeoPixelClear()
                Tackles = 0
                np[6] = (0,1,0)
        elif TotalTackles == 15:								
                NeoPixelClear()
                Tackles = 0
                np[6] = (1,0,1)
            
        
        if time.ticks_diff(time.ticks_ms(), timeLastToggleGPS) > 4000: 
            Stage = Stage + 1									  	   
            print("Current stage = ")
            print(Stage)
            timeLastToggleGPS = time.ticks_ms()						  											
            if Stage == 1: 										  	   
                mqtt.web_print(getBattery())						   
                lat1 = gps.get_latitude()							  
                lon1 = gps.get_longitude()							    
            if Stage == 2:											   
                gps_ticks()											  
                mqtt.web_print(gps_ticks(), 'oqoqo/feeds/iotmap1/csv') 
                lat2 = gps.get_latitude()							   
                lon2 = gps.get_longitude()							   
                TotalM = haversine(lon1, lat1, lon2, lat2) + TotalM   
                print("Total mængde meter rørt sig.")                  
                print(TotalM)										   
                print("Forventede hastighed")						   
                print(gps.get_speed())								   
            if Stage == 3: 										  	    
                mqtt.web_print(TotalM, 'oqoqo/feeds/iotproj1')
                Stage = 0	
            if TotalM > 100 and TotalM < 1000:
                    np[0] = (1,0,1)
                    np.write()
            elif TotalM > 1000 and TotalM < 2000: 
                    np[0] = (0,1,0)
                    np.write()
            elif TotalM > 2000 and TotalM < 3000:
                    np[0] = (0,0,1)
                    np.write()
            elif TotalM > 3000:
                    np[0] = (1,1,1)
                    np.write()
        
            
        if len(mqtt.besked) != 0: 
            mqtt.besked = ""
            
        mqtt.sync_with_adafruitIO()               
    
    except KeyboardInterrupt: 
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()