from machine import I2C
from time import sleep

#OBJECTS AND VARIABLES
i2c = I2C (0)
# I2C H/w 0, http://docs.micropython.org/en/late
print("Running I2c scanner\n")
while True:
#Scan for connected devices
    devices_identified = i2c.scan()
    #Print the result
    devices_count = len(devices_identified)
    print("Total number of devices: %d" % devices_count)

    if devices_count == 112: # There are 16 reserved addresses, thus not 128!
        print ("Looks like the I2C bus pull-up resistors are missing")
    else:
        for i in range (devices_count):
            print ("Device found at address: 0x%02x" % devices_identified[i])

print ()
#Blank line before next scan
sleep(1)