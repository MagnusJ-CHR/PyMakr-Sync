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
import _thread

i2c= I2C(0)

imu = MPU6050(i2c)
while True:
    accelerometer = imu.get_values #Laver en variabel med værdierne fra IMU accelerometererometer
    print(accelerometer())
