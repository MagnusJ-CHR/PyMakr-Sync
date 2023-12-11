from machine import Pin,ADC
from time import sleep
class LMT84Example:
    
    def __init__(self, pin_number=35, atten=2, ADC2_mV = 2048 / 4095, alpha = -4.85, beta = 1034, average = 128):
        self.pin_number = pin_number
        self.lmt84_ADC = ADC(Pin(pin_number, Pin.IN))
        self.lmt84_ADC.atten(atten)
        self.ADC2_mV = ADC2_mV
        self.alpha = alpha
        self.beta = beta
        self.average = average
        
        self.temp_celsius = None
        self.temp_fahrenheit = None
        self.temp_kelvin = None
        
    def get_temp_celsius(self):
        ADC_value = 0
        if self.average > 1:
            for i in range (self.average):
                ADC_value += self.lmt84_ADC.read()
                sleep(1 / self.average)
            ADC_value = ADC_value / self.average
        else:
            ADC_value = self.lmt84_ADC.read()
            sleep(1)
            
        mV = self.ADC2_mV * ADC_value
        temp = (mV - self.beta) / self.alpha
        print("Celsius Temp Is")
        return temp
    def get_temp_fahrenheit(self):
        ADC_value = 0
        if self.average > 1:
            for i in range (self.average):
                ADC_value += self.lmt84_ADC.read()
                sleep(1 / self.average)
            ADC_value = ADC_value / self.average
        else:
            ADC_value = self.lmt84_ADC.read()
            sleep(1)
            
        mV = self.ADC2_mV * ADC_value
        temp = (mV - self.beta) / self.alpha
        tempfahrenheit = temp * 9/5 + 32
        print("Fahrenheit Temp Is")
        return tempfahrenheit

    def get_temp_kelvin(self):
        ADC_value = 0
        if self.average > 1:
            for i in range (self.average):
                ADC_value += self.lmt84_ADC.read()
                sleep(1 / self.average)
            ADC_value = ADC_value / self.average
        else:
            ADC_value = self.lmt84_ADC.read()
            sleep(1)
            
        mV = self.ADC2_mV * ADC_value
        temp = (mV - self.beta) / self.alpha
        tempkelvin = temp + 273.15
        print("Fahrenheit Temp Is")
        return tempkelvin
    
        
        
lmt84 = LMT84Example()
print(lmt84.pin_number)
print(lmt84.get_temp_celsius())
print(lmt84.get_temp_fahrenheit())
print(lmt84.get_temp_kelvin())

        
        
        