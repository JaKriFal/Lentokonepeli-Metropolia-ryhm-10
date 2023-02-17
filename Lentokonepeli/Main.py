# Tänne importit
import random
import mariadb
from prettytable import PrettyTable


yhteys = mariadb.connect(
         host='localhost',
         port= 3306,
         database='flight_game',
         user='user1',
         password='password1',
         autocommit=True
         )

# Tänne globaalien muuttujien alustaminen
vic_con = False

# Tänne funktiot

def valitsin(User): #nää on ihan placeholdereita vielä, tehdään kaikille toiminnoille omat funktiot Userille
    print("Valitse komento: \n Lennä \n Tiedot \n Apua \n Lopeta")
    valinta = input("Anna komento: ")
    if valinta == "Lennä":
        User.Lennä()
        User.Ryöstö()
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
        self.money = 4990000
        self.raha_kerroin = 15000 #upgrade
        self.time = 0
        self.nykyinen_lon = str(24.957996168)
        self.nykyinen_lat = str(60.316998732)
        self.airport_type = "medium_airport" #upgrade
        self.range = str(250) #upgrade
        self.maa = "FI"
        self.akun_varaustaso = self.range
        self.lataus_nopeus = 30 #upgrade
        self.player_location = "helsinki"
        self.upgrades = 0
        self.risk = 0
        self.risk_kerroin = random.randint(80,120) #upgrade
        self.co_2 = 0
        self.co_2_rate = 0.02 #upgrade
        self.vaikeus_aste = 5000000
        self.vic_con = False

    def Lennä(self):
        #lista riskeille
        riskit = []
    #pyydetään sql kentät tietyn etäisyyden päässä omasta sijainnista
        sql = "select name, latitude_deg, longitude_deg, "
        sql += "ST_Distance_Sphere( point ('" + self.nykyinen_lon + "','" + self.nykyinen_lat + "'),"
        sql += "point(longitude_deg, latitude_deg)) * .001"
        sql += "as `distance_in_km` from `airport` "
        sql += "where type = '" + self.airport_type + "'and iso_country = '" + self.maa + "'"
        sql += " having `distance_in_km` <= '" + self.range + "'"
        sql += "order by `distance_in_km` asc"

        # print(sql)
        kursori = yhteys.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchall()

    #luodaan uusi lista josta tehdään käyttäjälle näkyvä taulukko
        uusi_tulos = [(item[0], round(item[-1])) for item in tulos]
        table = PrettyTable()
        table.field_names = ["#", "Lentokentän nimi", "Etäisyys KM", "Riski jäädä kiinni %"]
        for i, row in enumerate(uusi_tulos):
            #lasketaan etäisyyden mukaan riski jokaiselle kentälle jäädä kiinni
            etäisyys = row[-1]
            risk = round((etäisyys / self.risk_kerroin) + self.risk, 2)
            riskit.append(risk)
            table.add_row([i + 1] + list(row) + [risk])

        print(table)

        #päivitetään useriin sijainti. pitää lisätä looppi jos antaa väärän arvon
        kohde = input("Anna kentän numero mille haluat liikkua: ")
        print(f"olet nyt kentällä {tulos[int(kohde) - 1][0]}")
        self.nykyinen_lon = str(tulos[int(kohde) - 1][2])
        self.nykyinen_lat = str(tulos[int(kohde) - 1][1])
        self.player_location = tulos[int(kohde) - 1][0]
    #kauanko lennossa kesti
        self.time = self.time + tulos[int(kohde) - 1][3] * 0.01
    #co2 päästöt
        self.co_2 = self.co_2 + tulos[int(kohde) - 1][3] * self.co_2_rate
    #paljonko akussa rangea lennon jälkeen
        self.akun_varaustaso = int(self.range) - tulos[int(kohde) - 1][3]
    #tallenetaan valitun kentän riski
        self.risk = riskit[int(kohde)-1]
        return

    def Ryöstö(self):
        while True:
            lataus_aika = (int(self.range) - int(self.akun_varaustaso)) / int(self.lataus_nopeus)
            valinta = input(f"haluatko tehdä ryöstön? \nRiskisi jäädä kiinni on {self.risk}. Y/N: ")
            if valinta == "Y":
                if self.risk <= random.randint(0, 100):
                    print("onnistuit ryöstössäsi")
                    self.money = self.money + self.risk * self.raha_kerroin
                    print(f"sait ryöstettyä {round(self.risk * self.raha_kerroin)}€")
                else:
                    print("jäit kiinni")
                    self.money = self.money - self.risk * self.raha_kerroin * 2
                    print(f"menetit {round(self.risk * self.raha_kerroin * 2)}€")

                print(f"lentokoneen latauksessa kului {lataus_aika} tuntia")
                self.time = self.time + lataus_aika
                break

            elif valinta == "N":
                print(f"lentokoneen latauksessa kului {lataus_aika} tuntia")
                self.time = self.time + lataus_aika
                break
            else:
                print("komentoa ei tunnistettu")
        return

    def lopeta_peli(self):
        quitornot = input("Lopetetaanko peli? Y/N: ")
        if quitornot == "Y":
            self.vic_con = True
        elif quitornot == "N":
            self.vic_con = False
        else:
            print("Komentoa ei tunnistettu")

    def tulosta_tiedot(self):
        print(f"Pelaajan nimi on {self.name}, \nPaikka on {self.player_location},\nAikaa on kulunut {self.time} tuntia \n"
              f"CO2 päästösi ovat {self.co_2} tonnia \nrahamäärä on {round(self.money)}€")

#Pelin alustus(mm. kysytään pelaajalta nimi ja optionssit yms yms

name = input("Anna pelaajan nimi:")

Pelaaja = User(name)

# Main loop
while Pelaaja.vic_con == False:
    valitsin(Pelaaja)
    Pelaaja.vic_con = Pelaaja.money >= Pelaaja.vaikeus_aste



#Tänne toiminnot jotka ajetaan kun pelikerta päättyy
print("voiti pelin. sinun tuloksesi ovat:")
print(f"ryöstit {round(Pelaaja.money)}€")
print(f"sinun co2 jälkesi oli {round(Pelaaja.co_2)} tonnia")
print(f"sinun aikasi oli {round(Pelaaja.time)} tuntia")

