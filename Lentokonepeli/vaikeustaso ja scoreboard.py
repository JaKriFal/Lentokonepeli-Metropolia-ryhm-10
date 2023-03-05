import mariadb

yhteys = mariadb.connect(
         host='localhost',
         port= 3306,
         database='flight_game',
         user='user1',
         password='password1',
         autocommit=True
         )

easy = 5000000
medium = 75000000
hard = 10000000

difficulty = input("Valitse vaikeustaso: Helppo(h), keskitaso(k) vai vaikea(v)?")

if difficulty == "h":
    score_requirement = easy
elif difficulty == "k":
    score_requirement = medium
elif difficulty == "v":
    score_requirement = hard
else:
    print("Virheellinen syöte, kokeile uudelleen.")
    exit()



scoreboard = {}

final_score=score_requirement
name = input("Syötä pelaajan nimi: ")
score = int(final_score)
scoreboard[name] = score

print("\nTu:")
for name, score in scoreboard.items():
    print(f"{name}: {score}")


cursor = conn.cursor()


if difficulty == 'h':
    table_name = 'easy_scores'
elif difficulty == 'k':
    table_name = 'medium_scores'
else:
    difficulty == 'v'
    table_name = 'hard_scores'
    exit()

sql = f"INSERT INTO {table_name} (name, final_score, difficulty) VALUES (%s, %s, %s)"
values = (name, final_score, difficulty)
cursor.execute(sql, values)


cursor.close()
conn.close()

print("Tulos lisätty", table_name, "tietokantaan")