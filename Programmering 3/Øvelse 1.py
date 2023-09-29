from random import choice #Importerer de libraries vi behøver
dice = [0, 1, 2, 3, 4, 5] # Her laver vi en variabel som er mellem 0-5 beroende på choice funktionen

#1.1
Testliste1 = ["Banan","Aprikos","Fortnite"] # Her laver vi en liste
Testliste1.append("I love fortnite!") #Appender vi en extra string til vores liste
print(Testliste1) # Printer listen
#1.2
print(Testliste1[1]) #Printer item nummer 1 i liste
#1.3
Testliste1[2] = ("Gaming!") # Ændrer item nummer 2 til "Gaming!"
print(Testliste1[2]) #Printer den item
#1.4
Testliste2 = ["Ha!","Av!","Ha!","Host!","Host!","Ha!"] # Her skaber vi en liste med identiske entries
print(Testliste2)                                           #selv om de har samme navn, og printer dem
#1.5
print(Testliste2[choice(Dice)]) #Her bruger vi vores "Dice" funktion og skriver ud en random entry/item
#Fra vores liste