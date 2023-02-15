import mysql.connector
import random

nordic_countries = {'Denmark': 'DK', 'Finland': 'FI', 'Iceland': 'IS', 'Norway': 'NO', 'Sweden': 'SE'}
country = input(f"Choose a Nordic countrycode to get a spawn location, DK, FI, IS, NO or SE ({', '.join(nordic_countries.keys())}): ")


def get_airport(country_code):
    conn = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        database='flight_game',
        user='user1',
        password='password1',
        autocommit=True
    )

    cursor = conn.cursor()

    cursor.execute("SELECT name, ident FROM airport WHERE iso_country = %s", (country_code,))
    results = cursor.fetchall()

    if len(results) == 0:
        print("No airports found for that country.")
    else:
        airport = random.choice(results)
        print("Aloitus lentokenttäsi on: ", airport)

get_airport(country)