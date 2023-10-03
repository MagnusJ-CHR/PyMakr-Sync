import umqtt_robust2 as mqtt
from machine import Pin
from machine import PWM
from time import sleep

BUZZ_PIN = 26 # BUZZ Pin definition
buzzer_pin = Pin(BUZZ_PIN, Pin.OUT) # Desse kan vi bruger senere da de er defineret
pwm_buzz = PWM(buzzer_pin) # Igen, vi bruger disse senere

def buzzer(buzzer_PWM_object, frequency, sound_duration, silence_duration): # Definerer alle parameter for toner, og hvordan vi kan ændre tid, frekvens og mere på buzzern.
    buzzer_PWM_object.duty(512)
    buzzer_PWM_object.freq(frequency) 
    sleep(sound_duration)
    buzzer_PWM_object.duty(0)
    sleep(silence_duration)
buzzer(pwm_buzz, 1, 0.1, 0) # Stopper Buzzer fra at spille en lav tone 24/7



while True:
    try:
        
        if mqtt.besked == "beep!": # Hvis knap sender "beep!" så spiller vores buzzer en lille tone i 0.2 sekunder.
            print("Beep beep!")
            buzzer(pwm_buzz, 440, 0.2, 0.2)
            
        mqtt.sync_with_adafruitIO() # igangsæt at sende og modtage data med Adafruit IO             
        sleep(1) # Udkommentér denne og næste linje for at se visuelt output
        print(".", end = '') # printer et punktum til shell, uden et enter        
    
    except KeyboardInterrupt: # Stopper programmet når der trykkes Ctrl + c
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()