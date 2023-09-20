import umqtt_robust2 as mqtt
from machine import Pin
from machine import PWM
from time import sleep

led1 = Pin(26, Pin.OUT) # Definerer Pin

# Her kan i placere globale varibaler, og instanser af klasser

while True:
    try:
        # Indskriv egen kode her:
            
        if mqtt.besked == "led_on": # Hvis vi modtager led_on, så tænder lyset.
            led1.on()
        elif mqtt.besked == "led_off": # Modsat, modtager vi led_off så slukker lyset.
            led1.off()
            
        mqtt.sync_with_adafruitIO() # igangsæt at sende og modtage data med Adafruit IO             
        sleep(1) # Udkommentér denne og næste linje for at se visuelt output
        print(".", end = '') # printer et punktum til shell, uden et enter        
    
    except KeyboardInterrupt: # Stopper programmet når der trykkes Ctrl + c
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()