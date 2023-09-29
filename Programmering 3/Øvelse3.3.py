import machine, neopixel #Importerer de libraries vi behøver
import time

# number of pixels
n = 12
# strip control gpio
p = 26
np = neopixel.NeoPixel(machine.Pin(p), n)
# set single pixel (1st pixel = index [0]) to red color
np[0] = (255, 0, 0)
np.write()
time.sleep(1)

def fade_in_out(color, wait):  #En funktion for at lave en fade in og fade out.
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

fade_in_out('red', 5) #Laver en fade in og out, 5ms i rød farve
fade_in_out('green', 10)#Laver en fade in og out, 10ms i grøn farve
fade_in_out('blue', 25)#Laver en fade in og out, 25ms i blå farve
fade_in_out('purple', 30)#Laver en fade in og out, 30ms i lila farve
fade_in_out('yellow', 10)#Laver en fade in og out, 10ms i gul farve
fade_in_out('teal', 10)#Laver en fade in og out, 10ms i blågrøn farve
fade_in_out('white', 10)#Laver en fade in og out, 10ms i hvid farve
