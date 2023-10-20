from machine import I2C
from time import sleep_ms,sleep
import sys,uselect
from machine import UART
from machine import ADC
from machine import Pin

eeprom_i2c_addr = 0x50
eeprom_mem_address = 0x01
eeprom_mem_addressgroup = 0x01
eeprom_mem_addressBAT = 0x02


def hashnumbers(inputString):
    return [char for char in inputString if char.isdigit()]

print(hashnumbers("super string"))    # []


def write_byte(i2cAddr, addr, val):
    ba = bytearray(1)
    ba[0] = val
    res = i2c.writeto_mem(i2cAddr, addr, ba, addrsize = 16)
    sleep_ms(5)
    return res
def read_byte(i2cAddr, addr):
    val = i2c.readfrom_mem(i2cAddr, addr, 1, addrsize = 16)
    return val[0]

def har_tal(inputString):
    return any(char.isdigit() for char in string)

spanding = ADC(Pin(25, Pin.IN),atten=3)
spanding.atten(ADC.ATTN_11DB)
spanding.width(ADC.WIDTH_12BIT)
i2c = I2C (0)

uart_remote_port = 1
uart_remote_pin_tx = 33
uart_remote_pin_rx = 32
uart_remote_speed = 9600

group_id = 99

uart_remote = UART(uart_remote_port, baudrate = uart_remote_speed, tx = uart_remote_pin_tx, rx = uart_remote_pin_rx)

usb = uselect.poll()
usb.register(sys.stdin, uselect.POLLIN)

print("To vejs kommunikation skabt!(håber vi)")
while True:
    
    spanding_val = spanding.read()
    batteriniva = spanding_val * (3.3 / 4096)
    batstatus = '%.0f' % (batteriniva)
    batstat = str(batstatus)
    print(batteriniva)
    sleep(1)
#Scan for connected devices
    if uart_remote.any() > 0:
        string = uart_remote.read().decode()
        string = string.strip()
        print("REmote: " + string)
        
        if 'Batterystatus' in string.split():
            batstatus = '%.0f' % (batteriniva)
            batstat = str(batstatus)
            uart_remote.write(batstat + "%")
        if 'Gruppestatus' in string:
            uart_remote.write("Gruppe 5")
            
        if '%' in string:
            procentstat = string.strip("Remote" + "%")
            procentstore = int(procentstat)
            print(procentstore)
            write_byte(eeprom_i2c_addr, eeprom_mem_addressBAT, procentstore)
            value = read_byte(eeprom_i2c_addr, eeprom_mem_addressBAT)
            print("Modtager gruppe batteri er")
            print(value)
        
        
        if 'Gruppe' in string.split():
            savedgroup = int(hashnumbers(string)[0])
            write_byte(eeprom_i2c_addr, eeprom_mem_addressgroup, savedgroup)
            value = read_byte(eeprom_i2c_addr, eeprom_mem_address)
            print("Modtager grupper er sparet som")
            print(value)
            
            
    
    if usb.poll(0):
        string = sys.stdin.readline()
        sys.stdin.readline()
        string = string.strip()
        print("USB  : " + string)
        uart_remote.write(string + "\n")
        
        

   