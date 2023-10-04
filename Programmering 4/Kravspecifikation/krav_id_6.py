from socket import socket
from socket import AF_INET
from socket import SOCK_DGRAM
from sys import exit
from machine import Pin
from machine import PWM
from time import sleep
from random import choice
server_port = 12000
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(('', server_port))
print("Klar at modtage!")
dice = [110, 62, 262, 587, 659, 698]

BUZZ_PIN = 26 # BUZZ Pin definition
buzzer_pin = Pin(BUZZ_PIN, Pin.OUT) # Desse kan vi bruger senere da de er defineret
pwm_buzz = PWM(buzzer_pin) # Igen, vi bruger disse senere

def buzzer(buzzer_PWM_object, frequency, sound_duration, silence_duration): # Definerer alle parameter for toner, og hvordan vi kan ændre tid, frekvens og mere på buzzern.
    buzzer_PWM_object.duty(512)
    buzzer_PWM_object.freq(frequency) 
    sleep(sound_duration)
    buzzer_PWM_object.duty(0)
    sleep(silence_duration)
buzzer(pwm_buzz, choice(dice), 0.1, 0) # Stopper Buzzer fra at spille en lav tone 24/7


while True:
    try:
        message, client_address = server_socket.recvfrom(2048)
        modified_message = message. decode()
        server_socket.sendto(modified_message.encode(), client_address)
        if modified_message != "":
            print(modified_message)
            modified_message = ""
        if modified_message != "spil random toner":
            print(modified_message)
            print("beep!")
            modified_message = ""
            
            
            
    except KeyboardInterrupt:
        print("CTRL-C trykket, abort!")
        server_socket.close()
        exit()