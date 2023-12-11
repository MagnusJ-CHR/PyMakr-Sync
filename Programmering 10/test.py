from machine import Pin, deepsleep
from time import sleep,sleep_ms
import esp32
import random

IsRandom = 1
r = random.randint(0,1)
g = random.randint(0,1)
y = random.randint(0,1)
print(r)
print(y)
print(g)

red_pin = Pin(26, Pin.OUT)
ylw_pin = Pin(12, Pin.OUT)
grn_pin = Pin(13, Pin.OUT)
flashled = 0

wake_pin = Pin(4, Pin.IN, Pin.PULL_UP)
esp32.wake_on_ext0(pin = wake_pin,
                   level = esp32.WAKEUP_ALL_LOW)

while True:
    if IsRandom == 1:
        red_pin.value(r)
        sleep_ms(150)
        ylw_pin.value(y)
        sleep_ms(150)
        grn_pin.value(g)
        sleep_ms(150)