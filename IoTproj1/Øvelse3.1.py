from machine import I2C
from machine import Pin
from time import sleep,sleep_ms
from mpu6050 import MPU6050
import sys
import time
from neopixel import NeoPixel

timeLastToggle = 0

TacklingerTotal = 0
Tacklinger = 0
tacklet = 0

i2c= I2C(0)

imu = MPU6050(i2c)

n = 12 # Mængder pixel i ring
p = 26 #Pin i NeoPixel
np = NeoPixel(Pin(p, Pin.OUT), n) #Skabe NeoPixel instanse

def NeoPxTackling(r, g , b): # definition at tænde lamper 0-12
    if Tacklinger in range(1,6):
        np[Tacklinger] = (r, g , b)
        np.write()
def NeoPxClear():
    for i in range(0,12):
        np[i] = (0,0,0)
        np.write()

        

while True:
    try:
        #accel = imu.get_values
        sleep_ms(400)
        NeoPxTackling(100,0,0)
        np.write()
        if accel() > 10000  and  tacklet == 0:
            tacklet = 1
            Tacklinger = Tacklinger + 1
            TacklingerTotal = TacklingerTotal + 1
        if accel() in range(-9999,9999):
            tacklet = 0
        if accel() < -10000 and tacklet == 0:
            tacklet = 1
            Tacklinger = Tacklinger + 1
            TacklingerTotal = TacklingerTotal + 1
        if time.ticks_diff(time.ticks_ms(), timeLastToggle) > 1000:
            print("Totale maengde tacklinger \n" + str(TacklingerTotal))
            timeLastToggle = time.ticks_ms()
            if TacklingerTotal == 5:
                NeoPxClear()
                Tacklinger = 0
                np[6] = (0,0,255)
            if TacklingerTotal == 10:
                NeoPxClear()
                Tacklinger = 0
                np[6] = (0,255,0)
            if TacklingerTotal == 15:
                NeoPxClear()
                Tacklinger = 0
                np[6] = (0,255,255)
        
    except KeyboardInterrupt:
        print("Slukker.")
        sys.exit()