import umqtt_robust2 as mqtt
from machine import Pin
from machine import PWM
from time import sleep
from gpio_lcd import GpioLcd

lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
                d4_pin=Pin(33), d5_pin=Pin(32),
                  d6_pin=Pin(21), d7_pin=Pin(22),
                    num_lines=4, num_columns=20)

BUZZ_PIN = 26
buzzer_pin = Pin(BUZZ_PIN, Pin.OUT)
pwm_buzz = PWM(buzzer_pin)

def buzzer(buzzer_PWM_object, frequency, sound_duration, silence_duration):
    buzzer_PWM_object.duty(512)
    buzzer_PWM_object.freq(frequency)
    sleep(sound_duration)
    buzzer_PWM_object.duty(0)
    sleep(silence_duration)
buzzer(pwm_buzz, 1, 0.1, 0)

# Her kan i placere globale varibaler, og instanser af klasser

while True:
    try:
        # Indskriv egen kode her:
        lcd.clear()
        lcd.putstr(mqtt.besked) # Skriver altid den modtagne mqtt besked på LCD, så vi ved vad den arbejder med.
        ...
        if mqtt.besked == "incoming!": #Modtager vi denne, skriver vi vores tekst på  lcd og flasher den.
            buzzer(pwm_buzz, 780, 0.5, 0.2)
            lcd.putstr("Har jeg forstået opgaven korrekt?")
        ...         
        sleep (1)
            
        mqtt.sync_with_adafruitIO() # igangsæt at sende og modtage data med Adafruit IO             
        sleep(1) # Udkommentér denne og næste linje for at se visuelt output
        print(".", end = '') # printer et punktum til shell, uden et enter        
    
    except KeyboardInterrupt: # Stopper programmet når der trykkes Ctrl + c
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()