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

print("\nScoreboard:")
for name, score in scoreboard.items():
    print(f"{name}: {score}")