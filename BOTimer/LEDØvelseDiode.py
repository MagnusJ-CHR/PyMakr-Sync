from machine import Pin, PWM
from time import sleep
red_pin = Pin(18, Pin.OUT)
green_pin = Pin(19, Pin.OUT)
blue_pin = Pin(17, Pin.OUT)

red_freq = 1
red_duty = 512

blue_freq = 1
blue_duty = 512

green_freq = 40
green_duty = 1000

red = PWM(Pin(red_pin))
blue = PWM(Pin(blue_pin))
green = PWM(Pin(green_pin))

def decimaltoprct():
    nummer = input("Indsæt binært tal op til 1023.")
    decimal = int(nummer, 2)
    if decimal > 100:
        pass
    elif decimal <= 0:
        pass
    else:
        pct = decimal / 100
        omvandled = pct * 1023
        return omvandled
def prcttostyre():
    print("Indsæt rød % i binær")
    red_duty = decimaltoprct()
    print("Indsæt blå % i binær")
    blue_duty = decimaltoprct()
    print("Indsæt grøn % i binær")
    green_duty = decimaltoprct()
    sleep(2)
    red_freq = 10
    blue_freq = 20
    green_freq = 30
    print("Skal nu reflekteres.")

while True:
    prcttostyre()

    
