import mysql.connector

from prettytable import PrettyTable ,from_db_cursor


nykyinen_lon = "24.957996168"
nykyinen_lat = "60.316998732"
airport_type = "medium_airport"
etäisyys = "400"
maa = "FI"
def airports():
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
    print(tulos)

    uusi_tulos = [(item[0], item[-1]) for item in tulos]

    table = PrettyTable()
    table.field_names = ["#", "Lentokentän nimi", "Etäisyys"]
    for i, row in enumerate(uusi_tulos):
        table.add_row([i + 1] + list(row))

    print(tulos)
    print(table)
    return

yhteys = mysql.connector.connect(
         host='localhost',
         port= 3306,
         database='flight_game',
         user='user1',
         password='password1',
         autocommit=True
         )

airports()






