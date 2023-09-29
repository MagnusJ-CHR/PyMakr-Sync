import umqtt_robust2 as mqtt
import machine, neopixel
import time
from machine import Pin
from machine import PWM
from time import sleep
from gpio_lcd import GpioLcd
lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
                d4_pin=Pin(33), d5_pin=Pin(32),
                  d6_pin=Pin(21), d7_pin=Pin(22),
                    num_lines=4, num_columns=20)

# Her kan i placere globale varibaler, og instanser af klasser

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
# number of pixels
n = 12
# strip control gpio
p = 26
np = neopixel.NeoPixel(machine.Pin(p), n)
# set single pixel (1st pixel = index [0]) to red color
np[0] = (255, 0, 0)
np.write()
time.sleep(1)

def px012(r, g , b): # definition at tænde lamper 0-12 tilsammens
    for i in range(0,12):
        np[i] = (r, g , b)
        np.write()

def bounce(r, g, b): # Bounce funktion, farven hopper
    for i in range(4 * n):
        for j in range(n):
            np[j] = (r, g, b)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i% n) ] = (0, 0, 0)
        np.write()
        time.sleep_ms(40)

def wheel(pos): #Color wheel for vores regnbue at bruge
    #Indsæt fra 0-255, går fra RGB tilbage til R
    if pos < 0 or pos > 255:
        return (0,0,0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -=170
    return (pos * 3, 0, 255 - pos * 3)

def regnbue(wait): # Regnbue effekt, den skifter mellem gradienter og farver som en regnbue.
    for j in range(255):
        for i in range(n):
            rc_index = (i * 256 // n) + j
            np[i] = wheel (rc_index & 255)
        np.write()
        time.sleep_ms(wait)

regnbue(10)
regnbue(5)
time.sleep(1)

def fade_in_out(color, wait): # Fade in and out funktion, taler for sig selv
 for i in range(0, 4 * 256, 8):
  for j in range(n):
   if (i // 256) % 2 == 0:
    val = i & 0xff
   else:
     val = 255 - (i & 0xff)
     
     if color == 'red':
      np[j] = (val, 0, 0)
     elif color == 'green':
      np[j] = (0, val, 0)
     elif color == 'blue':
      np[j] = (0, 0, val)
     elif color == 'purple':
      np[j] = (val, 0, val)
     elif color == 'yellow':
      np[j] = (val, val, 0)
     elif color == 'teal':
      np[j] = (0, val, val)
     elif color == 'white':
      np[j] = (val, val, val)
     np.write()
  time.sleep_ms(wait)
  
while True:
    try:
        # Indskriv egen kode her:
        
        if mqtt.besked == "regnbue varning!": #Modtager den specifikke string, lav en lyd og brug regnbue effekt!
            lcd.putstr(mqtt.besked)
            buzzer(pwm_buzz, 100, 0.1, 0.4)
            wheel(180)
            regnbue(5)
            sleep(5)
            
        if mqtt.besked == "det hopper!": #Her laver vi en lyd hvis en specifik string modtages, + farven hopper.
            lcd.putstr(mqtt.besked)
            buzzer(pwm_buzz, 900, 0.5, 0.2)
            bounce(0,5,200)
        
        if mqtt.besked == "blå": # For at skifte til den specifikke farve (Blå), så laver vi farven blå.
            lcd.putstr("her kommer blå farve!")
            px012(0,0,255)
            
        
        
        if len(mqtt.besked) != 0: # Her nulstilles indkommende beskeder
            mqtt.besked = ""
            
        mqtt.sync_with_adafruitIO() # igangsæt at sende og modtage data med Adafruit IO             
        #sleep(1) # Udkommentér denne og næste linje for at se visuelt output
        #print(".", end = '') # printer et punktum til shell, uden et enter        
    
    except KeyboardInterrupt: # Stopper programmet når der trykkes Ctrl + c
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()