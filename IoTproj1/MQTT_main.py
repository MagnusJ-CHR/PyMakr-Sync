import umqtt_robust2 as mqtt
from machine import UART
from gps_bare_minimum import GPS_Minimum
import _thread
import time
from time import sleep,sleep_ms
from machine import I2C
from machine import Pin
from mpu6050 import MPU6050
import sys

spanding = ADC(Pin(25, Pin.IN),atten=3)
spanding.atten(ADC.ATTN_11DB)
spanding.width(ADC.WIDTH_12BIT)

i2c = I2C(0)

imu = MPU6050(i2c)

gps_port = 2                               # ESP32 UART port, Educaboard ESP32 default UART port
gps_speed = 9600                           # UART speed, defauls u-blox speed

uart = UART(gps_port, gps_speed)           # UART object creation
gps = GPS_Minimum(uart)                    # GPS object creation

# Her kan i placere globale variabler, og instanser af klasser
"""def get_adafruit_gps():
    speed = lat = lon = None
    if gps.receive_nmea_data():
        if gps.get_speed() != -999 and gps.get_latitude() != -999.0 and gps.get_longitude() != -999.0 and gps.get_validity() == "A":
            speed = str(gps.get_speed())
            lat = str(gps.get_latitude())
            lon = str(gps.get_longitude())
            return speed + "," + lat + "," + lon + "," + "0.0"
        else:
            print("Do it better!")
            return False
    else:
        return False
"""
while True:
    try:
        spanding_val = spanding.read()
        batteriniva = spanding_val * (3.3 / 4096)
        batteriniva = batteriniva * 1.4
        print(batteriniva)
        ootpoot = ((batteriniva - 3.0) / ( 4.2 - 3.0)) * 100
        print(ootpoot)
        sleep(1)
        
    
        
        """gps_data = get_adafruit_gps()
        if gps_data:
            print(f'\ngps_data er: {gps_data}')
            mqtt.web_print(get_adafruit_gps(), 'oqoqo/feeds/iotproj-1/csv')
            sleep(5)
        """
        
        
        mqtt.sync_with_adafruitIO() # igangsæt at sende og modtage data med Adafruit IO             
        #sleep(1) # Udkommentér denne og næste linje for at se visuelt output
        #print(".", end = '') # printer et punktum til shell, uden et enter        
    
    except KeyboardInterrupt: # Stopper programmet når der trykkes Ctrl + c
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()