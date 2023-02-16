import mysql.connector


nykyinen_lon = "24.957996168"
nykyinen_lat = "60.316998732"
airport_type = "medium_airport"
etäisyys = "2000"
def airports():
    sql = "select name, ST_Distance_Sphere( point ('" + nykyinen_lon +"','" + nykyinen_lat + "'),"
    sql += "point(longitude_deg, latitude_deg)) * .001"
    sql += "as `distance_in_km` from `airport` "
    sql += "where type = '" + airport_type + "' having `distance_in_km` <= '" + etäisyys + "'"
    sql += "order by `distance_in_km` asc"

    #print(sql)
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()

    return tulos

yhteys = mysql.connector.connect(
         host='localhost',
         port= 3306,
         database='flight_game',
         user='user1',
         password='password1',
         autocommit=True
         )

print(airports())




