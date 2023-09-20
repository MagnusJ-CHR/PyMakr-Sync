import machine, neopixel
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

def fade_in_out(color, wait):
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

fade_in_out('red', 5)
fade_in_out('green', 10)
fade_in_out('blue', 25)
fade_in_out('purple', 30)
fade_in_out('yellow', 10)
fade_in_out('teal', 10)
fade_in_out('white', 10)
