from dht import DHT11
from machine import Pin
import time

dht11 = DHT11(Pin(0, Pin.IN))
dht11.measure()

temp = dht11.temperature()
humid = dht11.humidity()

while True:
    print("Temperature", temp)
    time.sleep(3)