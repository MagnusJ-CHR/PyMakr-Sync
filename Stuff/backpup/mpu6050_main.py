from machine import I2C
from machine import Pin
from time import sleep,sleep_ms
from mpu6050 import MPU6050
import sys
import umqtt_robust2 as mqtt
#Initialisering af I2C objekt
i2c = I2C(0)     
#Initialisering af mpu6050 objekt
imu = MPU6050(i2c)
prone = 0
star = 0
antalgangelagt = 0

class status:
    ligger_ned = False


while True:
    try:
        # printer hele dictionary som returneres fra get_values metoden
        imu_data = imu.get_values()
        x = imu_data["acceleration z"]
        sleep_ms(100)
        
        if x > 7500 and x > 15000:
            print("Ligger ned")
            sleep(1)
            prone = 1
            
        elif x > 7500:
            print("Står")
            sleep(1)
            prone = 0
            status.ligger_ned = False
            
        if x < 7500 and x < -15000:
            print("Ligger ned")
            sleep(1)
            prone = 1
        elif x < 7500:
            print("Står")
            sleep(1)
            prone = 0
            status.ligger_ned = False
            
        if prone == 1 and status.ligger_ned == False:
            antalgangelagt = antalgangelagt + 1
            print("Mængde gange lagt sig ned")
            print(antalgangelagt)
            status.ligger_ned = True
            sleep(1)
            mqtt.web_print(antalgangelagt)
        
        
        
    except KeyboardInterrupt:
        print("Ctrl+C pressed - exiting program.")
        sys.exit()
