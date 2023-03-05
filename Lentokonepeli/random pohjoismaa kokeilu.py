import mariadb
import random

nordic_countries = {'Tanska': 'DK', 'Suomi': 'FI', 'Islanti': 'IS', 'Norja': 'NO', 'Ruotsi': 'SE'}
country = input(f"Valitse pohjoismaiden maakoodi saadaksesi aloitus lentokentän, DK, FI, IS, NO or SE ({', '.join(nordic_countries.keys())}): ")


def get_airport(country_code):
    conn = mariadb.connect(
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
        print("Ei lentokenttää maakoodilla.")
    else:
        airport = random.choice(results)
        print("Aloitus lentokenttäsi on: ", airport)

get_airport(country)