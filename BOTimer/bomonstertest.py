   batstatus = string
            batstat = str(batstatus)
            uart_remote.write(batstat + "%")
            hexbat = int(batstat)
            write_byte(eeprom_i2c_addr, eeprom_mem_addressBAT, hexbat)
            value = read_byte(eeprom_i2c_addr, eeprom_mem_addressBAT)
            print("Modtagere batteri er")
            print(value)