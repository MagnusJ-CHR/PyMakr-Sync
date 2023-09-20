import umqtt_robust2 as mqtt
from machine import Pin
from machine import PWM
from time import sleep
pb1=Pin(4, Pin.IN) # Første pushbutton initialiserer
pb2=Pin(0, Pin.IN) # Andre pushbutton initialiserer

# Her kan i placere globale varibaler, og instanser af klasser

while True: #Her bruger vi bare to forskellige PB for at endten be en kasse at skifte fra off til on (Skifte farve.)
    try:    
        
        sleep (0.1)
        if pb1.value() == 0: # Hvis pb1 bliver nertrykket, tænd med kommando "Adaon"
            mqtt.web_print("Adaon") # Sender Adaon
        if pb2.value() == 0: # Hvis PB2 bliver nertrykket, tænd med kommando "Adaoff"
            mqtt.web_print("Adaoff") #Sender adaoff
            
            mqtt.sync_with_adafruitIO() # igangsæt at sende og modtage data med Adafruit IO             
        sleep(1) # Udkommentér denne og næste linje for at se visuelt output
        print(".", end = '') # printer et punktum til shell, uden et enter        
    
    except KeyboardInterrupt: # Stopper programmet når der trykkes Ctrl + c
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()