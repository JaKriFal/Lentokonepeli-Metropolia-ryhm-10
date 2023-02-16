easy = 5000000
medium = 75000000
hard = 10000000

difficulty = input("Select a difficulty level: (Easy, medium or hard) ")

if difficulty == "easy":
    score_requirement = easy
elif difficulty == "medium":
    score_requirement = medium
elif difficulty == "hard":
    score_requirement = hard
else:
    print("Invalid difficulty level entered.")
    exit()

print(f"The score requirement for {difficulty} difficulty is {score_requirement}.")