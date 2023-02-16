# Tänne importit
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
        self.nykyinen_lon = str(24.957996168)
        self.nykyinen_lat = str(60.316998732)
        self.airport_type = "medium_airport"
        self.range = str(400)
        self.maa = "FI"
        self.player_location = "helsinki"
        self.upgrades = 0
        self.risk = 0
        self.co_2 = 0
        self.co_2_rate = 0.02
        self.vic_con = False

    def Lennä(self):

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
        uusi_tulos = [(item[0], item[-1]) for item in tulos]

        table = PrettyTable()
        table.field_names = ["#", "Lentokentän nimi", "Etäisyys KM"]
        for i, row in enumerate(uusi_tulos):
            table.add_row([i + 1] + list(row))
        print(table)

    #päivitetään useriin sijainti
        kohde = input("Anna kentän numero mille haluat liikkua: ")
        print(f"olet nyt kentällä {tulos[int(kohde) - 1][0]}")
        self.nykyinen_lon = str(tulos[int(kohde) - 1][2])
        self.nykyinen_lat = str(tulos[int(kohde) - 1][1])
        self.player_location = tulos[int(kohde) - 1][0]
    #kauanko lennosta kesti
        self.time = self.time + tulos[int(kohde) -1][3] * 0.5
    #co2 päästöt
        self.co_2 = tulos[int(kohde) -1][3] * self.co_2_rate
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
        print(f"Pelaajan nimi on {self.name}, \nPaikka on {self.player_location},\nAikaa on kulunut {self.time} min \n"
              f"CO2 päästösi ovat {self.co_2} tonnia \nja rahamäärä on {self.money}")

#Pelin alustus(mm. kysytään pelaajalta nimi ja optionssit yms yms

name = input("Anna pelaajan nimi:")

Pelaaja = User(name)

# Main loop
while Pelaaja.vic_con == False:
    valitsin(Pelaaja)


#Tänne toiminnot jotka ajetaan kun pelikerta päättyy


