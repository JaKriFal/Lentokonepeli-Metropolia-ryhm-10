# Tänne importit


# Tänne globaalien muuttujien alustaminen
vic_con = False

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

    def lopeta_peli(self):
        quitornot = input("Lopetetaanko peli? Y/N")
        if quitornot == "Y":
            return True
        elif quitornot == "N":
            return False
        else:
            print("Komentoa ei tunnistettu")
#Pelin alustus(mm. kysytään pelaajalta nimi ja optionssit yms yms

name = input("Anna pelaajan nimi:")

Pelaaja = User("name")

# Main loop
while vic_con == False:
    testi = Pelaaja.lopeta_peli()
    if testi:
        vic_conn = True
        print("Peli lopetettu")
    else:
        print("Peli jatkuu")


#Tänne toiminnot jotka ajetaan kun pelikerta päättyy
