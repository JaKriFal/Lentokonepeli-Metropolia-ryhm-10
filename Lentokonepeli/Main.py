# Tänne importit


# Tänne globaalien muuttujien alustaminen
vic_con = False

# Tänne funktiot

def valitsin(User): #nää on ihan placeholdereita vielä, tehdään kaikille toiminnoille omat funktiot Userille
    print("Valitse komento: \n Lennä \n Tiedot \n Apua \n Lopeta")
    valinta = input("Anna komento: ")
    if valinta == "Lennä":
        User.player_location = input("Anna kohde")
    elif valinta == "Tiedot":
        User.tulosta_tiedot()
    elif valinta == "Apua":
        print("APUVA!!!")
    elif valinta == "Lopeta":
        User.lopeta_peli()
    else:
        print("Komentoa ei tunnistettu")

# Tänne luokka-alustukset (varmaan lähinnä User/Pelaaja)

class User:
    def __init__(self, name):
        self.name = name
        self.money = 0
        self.time = 0
        self.player_location = "Helsinki"
        self.upgrades = 0
        self.risk = 0
        self.co_2 = 0
        self.co_2_rate = 0
        self.vic_con = False

    def lopeta_peli(self):
        quitornot = input("Lopetetaanko peli? Y/N: ")
        if quitornot == "Y":
            self.vic_con = True
        elif quitornot == "N":
            self.vic_con = False
        else:
            print("Komentoa ei tunnistettu")

    def tulosta_tiedot(self):
        print(f"Pelaajan nimi on {self.name}, paikka on {self.player_location} ja rahamäärä on {self.money}")

#Pelin alustus(mm. kysytään pelaajalta nimi ja optionssit yms yms

name = input("Anna pelaajan nimi:")

Pelaaja = User("name")

# Main loop
while Pelaaja.vic_con == False:
    valitsin(Pelaaja)


#Tänne toiminnot jotka ajetaan kun pelikerta päättyy
