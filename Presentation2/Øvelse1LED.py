import umqtt_robust2 as mqtt
from machine import Pin
from machine import PWM
from time import sleep

led1 = Pin(26, Pin.OUT) # Definerer Pin

while True:
    try:
            
        if mqtt.besked == "led_on": # Hvis vi modtager led_on, så tænder lyset.
            led1.on()
        elif mqtt.besked == "led_off": # Modsat, modtager vi led_off så slukker lyset.
            led1.off()
            
        mqtt.sync_with_adafruitIO()              
        sleep(1) 
        print(".", end = '') # printer et punktum til shell, uden et enter        
    
    except KeyboardInterrupt: # Stopper programmet når der trykkes Ctrl + c
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()