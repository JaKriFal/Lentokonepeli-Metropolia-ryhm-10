# Tänne importit


# Tänne globaalien muuttujien alustaminen
vic_con = False

# Tänne luokka-alustukset (varmaan lähinnä User/Pelaaja)

class User:
    def __init__(self, name, money, time, player_location, upgrades, risk, co_2):
        self.name = name
        self.money = money
        self.time = time
        self.player_location = player_location
        self.upgrades = upgrades
        self.risk = risk
        self.co_2 = co_2

    def lopeta_peli(self):
        return 0
#Pelin alustus(mm. kysytään pelaajalta nimi ja optionssit yms yms


# Main loop
while vic_con == False:
    print("looppi")


#Tänne toiminnot jotka ajetaan kun pelikerta päättyy
