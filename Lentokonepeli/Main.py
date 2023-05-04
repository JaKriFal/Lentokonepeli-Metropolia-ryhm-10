# Tänne importit
from flask import Flask, jsonify, request
import random
import mariadb
from prettytable import PrettyTable
# from weather import weather


yhteys = mariadb.connect(
    host='localhost',
    port=3306,
    database='flight_game',
    user='user1',
    password='password1',
    autocommit=True
)


# Tänne globaalien muuttujien alustaminen
vic_con = False

# Tänne funktiot


# nää on ihan placeholdereita vielä, tehdään kaikille toiminnoille omat funktiot Userille - Done
def event_selector(User):
    print("Valitse komento: \n Lennä \n Tiedot \n Päivitä \n Apua \n Lopeta")
    choice = input("Anna komento: ")
    if choice == "Lennä":
        # alle 300km etäisyydellä jää liian helposti yhden kentän ansaan joten maan vaihto aukeaa vasta ekan range upgrade jälkeen
        if int(User.range) > 300:
            change_country = input("Valitse haluatko vaihtaa maata. Y/N: ")
            if change_country == "Y":
                User.Change_country()
                User.move()
                User.Charging()
                User.Robbery()
            elif change_country == "N":
                User.move()
                User.Charging()
                User.Robbery()
            else:
                print("komentoa ei tunnistettu")
        else:
            User.move()
            User.Charging()
            User.Robbery()
    elif choice == "Kauppa":
        print("voit ostaa lentokoneen päivityksiä")
    elif choice == "Tiedot":
        User.get_info()
    elif choice == "Päivitä":
        User.plane_upgrade()
    elif choice == "Apua":
        User.help()
    elif choice == "Lopeta":
        User.end_game()
    else:
        print("Komentoa ei tunnistettu")

# Tänne luokka-alustukset (varmaan lähinnä User/Pelaaja)


class User:
    def __init__(self, name):
        self.game_on = True
        self.name = name
        self.money = 4500000
        # upgrade kentän riski * tämä = paljonko rahaa saa ryöstöstä
        self.money_factor = random.randint(12000, 17000)
        self.time = 0
        self.current_lon = str(24.957996168)
        self.current_lat = str(60.316998732)
        self.airport_type = "small_airport"  # upgrade
        self.range = str(250)  # upgrade
        self.current_country = "FI"
        self.battery_charge_level = self.range
        self.battery_charging_rate = 30  # upgrade montako kilsaa tulee tunnissa rangea
        self.player_location = "helsinki"
        self.upgrades = {"money_factor": False, "airport_type": True, "range": False, "battery_charging_rate": False,
                         "risk_factor": False, "co_2_rate": False, "flight_speed": False}
        self.risk = 0
        # upgrade arpoo riskiä kentälle etäisyys / risk factor
        self.risk_factor = random.randint(80, 120)
        self.co_2 = 0
        self.co_2_rate = 0.02  # upgrade  etäisyys kertaa tämä on montako tonnia co2 tulee
        # upgrade  etäisyys kertaa tämä on montako tuntia kesti lennossa
        self.flight_speed = 0.01
        self.difficulty = 5000000
        self.vic_con = False
        self.weather = 0

    def get_score(self):
        return float(self.money - self.time * 10 - self.co_2 * 15)

    def move(self):
        # lista riskeille
        risk_list = []
    # pyydetään sql kentät tietyn etäisyyden päässä omasta sijainnista
        sql = "select name, latitude_deg, longitude_deg, "
        sql += "ST_Distance_Sphere( point ('" + \
            self.current_lon + "','" + self.current_lat + "'),"
        sql += "point(longitude_deg, latitude_deg)) * .001"
        sql += "as `distance_in_km` from `airport` "
        sql += "where type = '" + self.airport_type + \
            "'and iso_country = '" + self.current_country + "'"
        sql += " having `distance_in_km` <= '" + \
            str(self.battery_charge_level) + "'"
        sql += "order by `distance_in_km` asc"

        # print(sql)
        kursori = yhteys.cursor()
        kursori.execute(sql)
        result = kursori.fetchall()

    # luodaan uusi lista josta tehdään käyttäjälle näkyvä taulukko
        user_result = [(item[0], round(item[-1])) for item in result]
        table = PrettyTable()
        table.field_names = ["#", "Lentokentän nimi",
                             "Etäisyys KM", "Riski jäädä kiinni %"]
        for i, row in enumerate(user_result):
            # lasketaan etäisyyden mukaan riski jokaiselle kentälle jäädä kiinni
            distance = row[-1]
            risk = round((distance / self.risk_factor) + self.risk, 2)
            risk_list.append(risk)
            table.add_row([i + 1] + list(row) + [risk])
        print(table)

        # kysytään mihin kentälle halutaan
        target = input("Anna kentän numero mille haluat liikkua: ")
        while not target.isnumeric() or not (1 <= int(target) <= len(user_result)):
            print("Virheellinen syöte")
            target = input("Anna kentän numero mille haluat liikkua: ")
        print(
            f"Lennossa kesti {round(result[int(target) - 1][3] * self.flight_speed, 1)} tuntia")
        print(f"Olet nyt kentällä {result[int(target) - 1][0]}")

    # päivitetään oma sijainti
        self.current_lon = str(result[int(target) - 1][2])
        self.current_lat = str(result[int(target) - 1][1])
        self.player_location = result[int(target) - 1][0]
    # kauanko lennossa kesti
        self.time = self.time + result[int(target) - 1][3] * 0.01
    # co2 päästöt
        self.co_2 = self.co_2 + result[int(target) - 1][3] * self.co_2_rate
    # paljonko akussa rangea lennon jälkeen
        self.battery_charge_level = int(
            self.range) - result[int(target) - 1][3]
    # tallenetaan valitun kentän riski
        self.risk = risk_list[int(target)-1]

    # printataan sää
        # weather(self.player_location)
        return

    def Robbery(self):
        choice = "x"
        while choice != "Y" and choice != "N":
            # charging_time = (int(self.range) - int(self.battery_charge_level)) / int(self.battery_charging_rate)
            choice = input(
                f"Haluatko tehdä ryöstön? \nRiskisi jäädä kiinni on {self.risk}. Y/N: ")
            if choice == "Y":
                # tehdään ryöstö. chekataan onnistuko ryöstö ja päivitetään rahat sekä latauksee kulunu aika
                if self.risk <= random.randint(0, 100):
                    print("onnistuit ryöstössäsi")
                    self.money = self.money + self.risk * self.money_factor
                    print(
                        f"Sait ryöstettyä {round(self.risk * self.money_factor)}€")
                else:
                    # ryöstö epäonnistu. miinustetaan rahat ja päivitetään latauksee kulunu aika
                    print("Jäit kiinni")
                    self.money = self.money - self.risk * self.money_factor * 2
                    print(
                        f"Menetit {round(self.risk * self.money_factor * 2)}€")

            elif choice == "N":
                return
            else:
                print("Komentoa ei tunnistettu")
        return

    def Charging(self):
        choice = ""
        while choice != "Y" and choice != "N":
            charging_time = (int(
                self.range) - int(self.battery_charge_level)) / int(self.battery_charging_rate)
            choice = input(f"Haluatko ladata lentokonettasi? Sinulla on {round(int(self.battery_charge_level))} KM akkua jäljellä. \n"
                           f"Akun täyteen lataaminen kestäisi {round(charging_time)} tuntia. Y/N: ")
            if choice == "Y":
                print(
                    f"Lentokoneen akku on nyt täynnä. Latauksessa kesti {round(charging_time)}")
                self.time = self.time + charging_time
                self.battery_charge_level = self.range
            elif choice == "N":
                return
            else:
                print("Komentoa ei tunnistettu")
        return

    def Change_country(self):
        # haetaan tietokannoista lista maista joilla on lentokenttä koneen rangen sisällä
        sql = "SELECT iso_country, COUNT(*) AS airport_count "
        sql += "FROM airport "
        sql += "WHERE type = '" + self.airport_type + "' "
        sql += "AND iso_country != '" + self.current_country + "' "
        sql += "AND ST_Distance_Sphere(point('" + \
            self.current_lon + "','" + self.current_lat + "'), "
        sql += "point(longitude_deg, latitude_deg)) * 0.001 <= " + \
            str(self.range)
        sql += " GROUP BY iso_country"

        kursori = yhteys.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchall()

        # taulokko maista ja montako kenttää siellä on rangen kantamalla
        table = PrettyTable()
        table.field_names = ["Maakoodi", "Kenttien määrä"]
        for rivi in tulos:
            table.add_row([rivi[0], rivi[1]])
        print(table)
        # valitaan maa mihin lennetään
        countries = [t[0] for t in tulos]
        country = ""
        while country not in countries:
            country = input("Anna maakoodi johon haluat matkustaa: ")
            self.current_country = country
            if country not in countries:
                print("Virheellinen maakoodi. Anna uusi maakoodi.")
        # nollataan riski
        self.risk = 0
        return

    def help(self):
        print(f"Pelissä sinun on tarkoitus kerätä rahaa {self.difficulty}€ verran ryöstelemällä lentokenttiä. \nJos haluat ryöstää lentokentän"
              f" valitse valikosta Lennä. Komento vie sinut valitsemallesi lentokentälle\nListassa näet lentokenttiä, niiden etäisyydet"
              f" sekä riskin jäädä kiinni ryöstöstä. \nValittuasi kenttää vastaavan numeron, sinulla on mahdollisuus ryöstää kenttä."
              f"\nJos ryöstö onnistui, sinä saat ilmoitetun määrän rahaa. Jos taas ryöstö epäonnistui, joudut lahjomaan tuomarin ja menetät rahaa"
              f"\nVoit myös päivittää lentokoneesi ominaisuuksia jokaisella lentokentällä.")
        return

    def end_game(self):
        quitornot = input("Lopetetaanko peli? Y/N: ")
        if quitornot == "Y":
            self.game_on = False
        elif quitornot == "N":
            self.game_on = True
        else:
            print("Komentoa ei tunnistettu")

    def get_info(self):
        print(f"Pelaajan nimi on {self.name}, \nPaikka on {self.player_location},\nAikaa on kulunut {round(self.time)} tuntia \n"
              f"CO2 päästösi ovat {round(self.co_2)} tonnia \nRahamäärä on {round(self.money)} € \nTämän hetkinen pistemäärä on {self.get_score()}")

    # lentokoneen päivitysfunktio
    def plane_upgrade(self):
        # tarkistaa sanakirjasta mitä päivityksiä saatavilla
        print("Kaikki päivitykset maksavat 100000€. Saatavilla olevat päivitykset:")
        for x in self.upgrades:  # looppi printtaa päivitykset
            if self.upgrades[x] == False:
                print(x)
        selected_upgrade = input(
            "Anna haluamasi päivitys, 'Info' saadaksesi lisätietoja tai 'Peruuta' peruuttaaksesi päivityksen: ")
        if selected_upgrade == 'Peruuta':
            print("Päivitys peruutettu.")
        elif selected_upgrade == 'Info':
            print("'money_factor' lisää ryöstöistä saatua rahamäärää. \n'range' lisää lentokoneesi kantomatkaa.\n'battery_charging_rate' lisää akun latausnopeutta\n'risk_factor' vähentää kiinnijäämisriskiä.\n'co_2_rate' vähentää lentokoneesi päästöjä.\n'flight_speed' lisää lentokoneesi nopeutta. ")
            return
        elif selected_upgrade == "money_factor":
            if self.money < 100000:
                print("Ei rahaa päivitykseen.")
                return
            print(selected_upgrade + " valittu!")
            self.upgrades[selected_upgrade] = True
            self.money_factor = self.money_factor + 2000
            self.money -= 100000
        elif selected_upgrade == "airport_type":
            if self.money < 100000:
                print("Ei rahaa päivitykseen.")
                return
            print(selected_upgrade + " valittu!")
            self.upgrades[selected_upgrade] = True
            self.airport_type = self.airport_type + ""
            self.money -= 100000
        elif selected_upgrade == "range":
            if self.money < 100000:
                print("Ei rahaa päivitykseen.")
                return
            print(selected_upgrade + " valittu!")
            self.upgrades[selected_upgrade] = True
            self.range = "300"
            self.money -= 100000
        elif selected_upgrade == "battery_charging_rate":
            if self.money < 100000:
                print("Ei rahaa päivitykseen.")
                return
            print(selected_upgrade + " valittu!")
            self.upgrades[selected_upgrade] = True
            self.battery_charging_rate = self.battery_charging_rate + 10
            self.money -= 100000
        elif selected_upgrade == "risk_factor":
            if self.money < 100000:
                print("Ei rahaa päivitykseen.")
                return
            print(selected_upgrade + " valittu!")
            self.upgrades[selected_upgrade] = True
            self.risk_factor = self.risk_factor + 20
            self.money -= 100000
        elif selected_upgrade == "co_2_rate":
            if self.money < 100000:
                print("Ei rahaa päivitykseen.")
                return
            print(selected_upgrade + " valittu!")
            self.upgrades[selected_upgrade] = True
            self.co_2_rate = self.co_2_rate + 0.01
            self.money -= 100000
        elif selected_upgrade == "flight_speed":
            if self.money < 100000:
                print("Ei rahaa päivitykseen.")
                return
            print(selected_upgrade + " valittu!")
            self.upgrades[selected_upgrade] = True
            self.flight_speed = self.flight_speed + 0.01
            self.money -= 100000
        else:
            print("Komentoa ei tunnistettu, palataan toimintavalikkoon.")
        return


# Pelin alustus(mm. kysytään pelaajalta nimi ja optionssit yms yms
print(f"Tervetuloa Lentokonepeli-protoon, pelin tavoite on saada kasaan 5000000€ tekemällä ryöstöjä eri kaupungeissa.")

name = input("Anna pelaajan nimi: ")

Player = User(name)

# Main loop
while Player.game_on:
    event_selector(Player)
    if Player.money >= Player.difficulty:
        Player.vic_con = True
        Player.game_on = False


# Tänne toiminnot jotka ajetaan kun pelikerta päättyy
if Player.vic_con:
    print("Voitit pelin! sinun tuloksesi ovat:")
    print(f"ryöstit {round(Player.money)}€")
    print(f"Sinun co2 jälkesi oli {round(Player.co_2)} tonnia")
    print(f"Sinun aikasi oli {round(Player.time)} tuntia")
    print(f"kokonaispisteesi olivat {Player.get_score}")
else:
    print("Peli lopetettu.")
