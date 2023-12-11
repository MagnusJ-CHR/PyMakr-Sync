class OhmLaw:
    def __init__(self, volt = 0,ampere = 0,ohm = 0, watt = 0):
        self.volt = volt
        self.ampere = ampere
        self.ohm = ohm
        self.watt = watt
    
    def resistance_volt_ampere(self, ):
        ohm = self.volt / self.ampere
        self.ohm = ohm
        print(self.volt,"v","/", self.ampere,"a")
        print("Resistance is")
        print(ohm)
        return ohm
    
    def volt_resistance_ampere(self, ):
        volt = self.ohm * self.ampere
        self.voltage = volt
        print(self.ohm,"ohm","*",self.ampere,"a")
        print("Volt is")
        print(volt)
        return volt
    def effect_volt_ampere(self, ):
        watt = self.volt * self.ampere
        self.watt = watt
        print(self.volt,"v","*",self.ampere,"a")
        print("Effect is")
        print(watt)
        return
    def ampere_effect_volt(self, ):
        ampere = self.watt / self.volt
        self.ampere = ampere
        print(self.watt,"w","/",self.volt,"v")
        print("Ampere is")
        print(ampere)
        return 
    
calculateohm = OhmLaw()

calculateohm.volt = 3
calculateohm.ampere = 0.05

calculateohm.resistance_volt_ampere()

calculateohm.volt_resistance_ampere()

calculateohm.effect_volt_ampere()

calculateohm.ampere_effect_volt()




        
    