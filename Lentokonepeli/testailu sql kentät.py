import mysql.connector



def airports():
    sql = "select name, ST_Distance_Sphere( point ('24.957996168', '60.316998732'), point(longitude_deg, latitude_deg)) * .001"
    sql += "as `distance_in_km` from `airport` where type = 'heliport' having `distance_in_km` <= '300'"
    sql += "order by `distance_in_km` asc"

    print(sql)
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()

    return tulos

yhteys = mysql.connector.connect(
         host='localhost',
         port= 3306,
         database='flight_game',
         user='max',
         password='password',
         autocommit=True
         )

print(airports())
