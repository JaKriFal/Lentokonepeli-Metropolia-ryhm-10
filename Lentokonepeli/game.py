import random
import mariadb
from prettytable import PrettyTable
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


yhteys = mariadb.connect(
    host='localhost',
    port=3306,
    database='flight_game',
    user='user1',
    password='password1',
    autocommit=True
)


class User:
    def __init__(self,):
        self.game_on = True
        self.name = "name"
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
        self.risk_list = []
        self.result = []

    def get_score(self):
        return float(self.money - self.time * 10 - self.co_2 * 15)

    def move(self,):
        # lista riskeille

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
        self.result = kursori.fetchall()

    # luodaan uusi lista josta tehdään käyttäjälle näkyvä taulukko
        user_result = [(item[0], round(item[-1])) for item in self.result]
        table = PrettyTable()
        table.field_names = ["#", "Lentokentän nimi",
                             "Etäisyys KM", "Riski jäädä kiinni %"]
        for i, row in enumerate(user_result):
            # lasketaan etäisyyden mukaan riski jokaiselle kentälle jäädä kiinni
            distance = row[-1]
            risk = round((distance / self.risk_factor) + self.risk, 2)
            self.risk_list.append(risk)
            table.add_row([i + 1] + list(row) + [risk])
        print(table)

        return self.result

    def upgrade_loc(self, target):
        # päivitetään oma sijainti
        self.current_lon = str(self.result[int(target) - 1][2])
        self.current_lat = str(self.result[int(target) - 1][1])
        self.player_location = self.result[int(target) - 1][0]
    # kauanko lennossa kesti
        self.time = self.time + self.result[int(target) - 1][3] * 0.01
    # co2 päästöt
        self.co_2 = self.co_2 + \
            self.result[int(target) - 1][3] * self.co_2_rate
    # paljonko akussa rangea lennon jälkeen
        self.battery_charge_level = int(
            self.range) - self.result[int(target) - 1][3]
    # tallenetaan valitun kentän riski
        self.risk = self.risk_list[int(target)-1]
        print(self.player_location)
        charging_time = (int(
            self.range) - int(self.battery_charge_level)) / int(self.battery_charging_rate)
        self.time = self.time + charging_time
        self.battery_charge_level = self.range

        return

    def Robbery(self):
        self.risk_list = []
        # charging_time = (int(self.range) - int(self.battery_charge_level)) / int(self.battery_charging_rate)

        # tehdään ryöstö. chekataan onnistuko ryöstö ja päivitetään rahat sekä latauksee kulunu aika
        if self.risk <= random.randint(0, 100):
            print("onnistuit ryöstössäsi")
            self.money = self.money + self.risk * self.money_factor
            how_much = self.risk * self.money_factor
            print(
                f"Sait ryöstettyä {round(self.risk * self.money_factor)}€")
            return True, how_much
        else:
            # ryöstö epäonnistu. miinustetaan rahat ja päivitetään latauksee kulunu aika
            print("Jäit kiinni")
            self.money = self.money - self.risk * self.money_factor * 2
            print(
                f"Menetit {round(self.risk * self.money_factor * 2)}€")
            how_much = self.risk * self.money_factor * 2
            self.risk = 0

        return False, how_much

    def Change_country(self):
        # haetaan tietokannoista lista maista joilla on lentokenttä koneen rangen sisällä
        sql = "SELECT iso_country "
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
        self.tulos = kursori.fetchall()
        return self.tulos

    def Change_country2(self, country):
        countries = [t[0] for t in self.tulos]
        if country in countries:
            self.current_country = country
            print(self.current_country)
            return
        # nollataan riski
        self.risk = 0


Player = User()


@app.route('/kokeilu5/<maakoodi>')
def vaihda_maa(maakoodi):       # vaihtaa maan

    Player.Change_country2(str(maakoodi))
    response = {
        'status': 'ok',


    }
    return jsonify(response)


@app.route('/kokeilu4/')
def Maan_vaihto():  # kertoo mihin maahan voi lentää
    Player.Change_country()
    testi = Player.Change_country()
    response = {
        'status': 'ok',
        "nykyinen_maa": Player.current_country,
        "nykyinen_sijainti": Player.player_location,
        "lista_maista_joihin_voi_lentää": testi,


    }
    return jsonify(response)


@app.route('/kokeilu3/')
def Testi():
    Player.Robbery()   # ryöstö ja kertoo paljonko rahaa menetit / rahatilanteen
    response = {
        'status': 'ok',
        "onnistuit": Player.Robbery()[0],
        "rahat": Player.money,
        "paljonko_rahaa_tuli/meni": Player.Robbery()[1],



    }
    return jsonify(response)


@app.route('/kokeilu2/<number>')  # lentää kentälle ja päivittää tiedot
def liiku(number):

    Player.upgrade_loc(int(number))
    response = {
        'status': 'ok',


    }
    print("Fly ok!")
    return jsonify(response)


# lista kentistä mihin voi lentää ja riski jäädä kiinni
@app.route('/kokeilu/')
def airports():

    curr = [Player.player_location, Player.current_lat, Player.current_lon]
    result = Player.move()

    response = {
        'status': 'ok',
        'omapaikka': curr,
        "lista_kentista": result,
        "riskilista_kentille": Player.risk_list,
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
