from hcsr04 import HCSR04
import uasyncio as asyncio
from gpio_lcd import GpioLcd
from machine import Pin,PWM
from time import sleep
import math

pb1=Pin(4, Pin.IN)

pin_led_red = 26
led_red = PWM(Pin(pin_led_red))

lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
              d4_pin=Pin(33), d5_pin=Pin(32),
              d6_pin=Pin(21), d7_pin=Pin(22),
              num_lines=4, num_columns=20,
              backlight_pin=Pin(23, Pin.OUT))


ultrasonic = HCSR04(15, 34)

async def distance():
    while True:
        lcd.clear
        lcd.move_to(0,0)
        distcm = round(ultrasonic.distance_cm())
        lcd.putstr(f"distance:{distcm} cm")
        await asyncio.sleep_ms(300)
        
async def pwmdistance():
    while True:
        distcm1 = round(ultrasonic.distance_cm())
        factor = distcm1 / 512
        brightnessfloat = factor * 512
        brightness = math.floor(brightnessfloat)
        led_red.freq(40)
        led_red.duty(brightness)
        await asyncio.sleep_ms(300)
        
async def buttondistance():
    while True:
        if pb1.value() == 0:
            distcm2 = round(ultrasonic.distance_cm())
            print(distcm2)
            if distcm2 < 30:
                lcd.clear()
                lcd.move_to(0,1)
                lcd.putstr("Back up!")
            elif distcm2 > 60:
                print("diller")
                lcd.move_to(0,1)
                lcd.putstr("Come closer!")
            else:
                lcd.move_to(0,1)
                lcd.putstr("A-ok distance.")
        
        await asyncio.sleep_ms(300)
        
        
        
    
loop = asyncio.get_event_loop()
loop.create_task(distance())
loop.create_task(pwmdistance())
loop.create_task(buttondistance())
loop.run_forever()