"""
Nedanstående kode bruger matematik for at finde ud hvor mange biler kan være i drift samt mængden passagererer som kan tas emod.
Samtidigt regner den ud hvor mange skal være i hver bil udfra hvor mange sæder og passagerere findes."""
"""TL;DR: Matematik bruges på en smart måde for at få en automatiseret måde at finde ud service-nivå den dag."""
"""Øvelse 3.1 er helt enkelt hvis man till exempel glemmer at definere "samlet_bil_kapacitet" inden man lægger den i sin kode.
Det kan også være at man fejlstaver eller glemmer det er case-sensetive."""

biler = 100
plads_i_en_bil = 4.0
førere = 30
passagerer = 90
biler_ude_af_drift = biler - førere
biler_i_kørsel = førere
samlet_bil_kapacitet = biler_i_kørsel * plads_i_en_bil
gennemsnit_af_passagerer_per_bil = passagerer / biler_i_kørsel

print("Der er", biler, " biler til rådighed.")
print("Der er kun", førere, "førere til rådighed.")
print("Der vil være", biler_ude_af_drift, "tomme biler i dag.")
print("Vi kan transportere", samlet_bil_kapacitet, "personer i dag.")
print("Vi har", passagerer, "passagerer i dag.")
print("Vi skal cirka putte", gennemsnit_af_passagerer_per_bil, " i hver bil.")
