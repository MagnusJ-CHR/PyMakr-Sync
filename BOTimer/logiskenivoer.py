from machine import Pin,ADC
from time import sleep

pot = ADC(Pin(34,Pin.IN),atten=3)
pot.atten(ADC.ATTN_11DB)
pot.width(ADC.WIDTH_12BIT)
output = Pin(19,Pin.OUT)

output.value(1)

while True:
    
    if pot.read() < 845:
        output.value(0)
    elif pot.read() > 3545:
        output.value(1)
    

