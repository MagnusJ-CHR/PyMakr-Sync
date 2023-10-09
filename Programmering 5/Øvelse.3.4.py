# GPS program
from machine import UART
import machine,neopixel
from gps_bare_minimum import GPS_Minimum
import _thread
from time import sleep,sleep_ms
import umqtt_robust2 as mqtt
import math
#kord 1
lat_1 = 55.694331
lon_1 = 12.548807
#kord 2
lat_2 = 55.693950
lon_2 = 12.547942
R = 0.0003

def indenfor_granse(lat_1, lon_1, lat_2, lon_2):
    a = lat_1 - lat_2
    b= lon_1 - lon_2
    a = abs(a)
    b = abs(b)
    c = math.sqrt((b**2) + (a**2))
    print(c)
    if c >= R:
        print("Udenfor granse!")
        return False
    if c < R:
        print("Indenfor granse!")
        return True




#########################################################################
# CONFIGURATION
gps_port = 2                               # ESP32 UART port, Educaboard ESP32 default UART port
gps_speed = 9600                           # UART speed, defauls u-blox speed
#########################################################################
# OBJECTS
uart = UART(gps_port, gps_speed)           # UART object creation
gps = GPS_Minimum(uart)                    # GPS object creation
#########################################################################    
#

# number of pixels
n = 12
# strip control gpio
p = 26
np = neopixel.NeoPixel(machine.Pin(p), n)
def bounce(r, g, b): # Bounce funktion, farven hopper
    for i in range(4 * n):
        for j in range(n):
            np[j] = (r, g, b)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i% n) ] = (0, 0, 0)
        np.write()
        sleep_ms(40)

def get_adafruit_gps():
    speed = lat = lon = None
    while True:
        if gps.receive_nmea_data():
            if gps.get_speed() != -999 and gps.get_latitude() != -999.0 and gps.get_longitude() != -999.0 and gps.get_validity() == "A":
                speed = str(gps.get_speed())
                lat = str(gps.get_latitude())
                lon = str(gps.get_longitude())
                return speed + "," + lat + "," + lon + "," + "0.0"
            elif gps.get_speed() == -999 and gps.get_latitude() == -999.0 and gps.get_longitude() == -999.0:
                print("Mangler opkobling mod satellit. Kom nærmere et vindue")
                bounce(255,0,0) # Samme som forrige opgave, hvis den bliver set som ugyldig kører vi bare en bounce med rød farve.
        else:
            return False
while True:
    try:
        gps_data = get_adafruit_gps()
        if gps_data:
            print(f'\n GPS_DATA er:{gps_data}')
            mqtt.web_print(get_adafruit_gps(), 'oqoqo/feeds/spfeed/csv')
            indenfor_granse(lat_1, lon_1, lat_2, lon_2)
            sleep(4)
            mqtt.web_print(gps.get_speed(), 'oqoqo/feeds/spfeed/csv') # Her bruger vi bare samme tanke som når vi gjorde vores map, men vi sender kun
            # vores hastigheds data til dette feed. HUSK! Behøver en sleep(4) før, ellers sender vi for hurtigt og ADAFRUIT bliver sur.
            bounce(0,255,0) # Samme som forrige opgave, hvis den bliver set som gyldig kører vi bare en bounce med grøn farve.
        sleep(4)
        if len(mqtt.besked) != 0:
            mqtt.besked = ""
        mqtt.sync_with_adafruitIO()
        print(".", end = '')
    
    except KeyboardInterrupt:
        print ('CTRL C trykket, avbruder!')
        mqtt.c.disconnect()
        mqtt.sys.exit()
 