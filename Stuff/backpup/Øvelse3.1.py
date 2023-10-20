from machine import I2C
from machine import Pin
from time import sleep,sleep_ms
from mpu6050 import MPU6050
import sys

i2c= I2C(0)
imu = MPU6050(i2c)

while true:
    try:
        print(imu.get_values())
        sleep_ms(10)
        
    except KeyboardInterrupt:
        print("Slukker.")
        sys.exit()