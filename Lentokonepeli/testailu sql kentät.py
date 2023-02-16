import mariadb
from prettytable import PrettyTable



def airports():
    nykyinen_lon = str(24.957996168)
    nykyinen_lat = str(60.316998732)
    airport_type = "medium_airport"
    etäisyys = "400"
    maa = "FI"

    sql = "select name, latitude_deg, longitude_deg, "
    sql += "ST_Distance_Sphere( point ('" + nykyinen_lon +"','" + nykyinen_lat + "'),"
    sql += "point(longitude_deg, latitude_deg)) * .001"
    sql += "as `distance_in_km` from `airport` "
    sql += "where type = '" + airport_type + "'and iso_country = '" + maa + "'"
    sql += " having `distance_in_km` <= '" + etäisyys + "'"
    sql += "order by `distance_in_km` asc"

    #print(sql)
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()


    uusi_tulos = [(item[0], item[-1]) for item in tulos]

    table = PrettyTable()
    table.field_names = ["#", "Lentokentän nimi", "Etäisyys KM"]
    for i, row in enumerate(uusi_tulos):
        table.add_row([i + 1] + list(row))
    print(table)

    kohde =input("Anna kentän numero mille haluat liikkua: ")
    print(f"olet nyt kentällä {tulos[int(kohde)-1][0]}")
    nykyinen_lon = tulos[int(kohde)-1][2]
    nykyinen_lat = tulos[int(kohde)-1][1]

    return

yhteys = mariadb.connect(
         host='localhost',
         port= 3306,
         database='flight_game',
         user='user1',
         password='password1',
         autocommit=True
         )

airports()






