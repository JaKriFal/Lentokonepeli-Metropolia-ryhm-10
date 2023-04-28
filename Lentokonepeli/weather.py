
from pip._vendor import requests
# Path: Lentokonepeli/Main.py


def Get_weather(player_location):
    city = player_location
# location = geocode(city)
# print(location.adress)

    weather = "https://api.openweathermap.org/data/2.5/weather?q=" + \
        city + "&lang=fi&APPID=7c449d15551f18e130e9229fa2887cc3"
    request = requests.get(weather).json()
# print(request)

    temperature = request["main"]
    celsius = temperature["temp"]
    final_temp = int(celsius) - 273.15
    desc_weather = request["weather"]
    desc2 = desc_weather[0]["description"]

    print("Sää " + city + " on " + str(final_temp) + " astetta ja " + desc2 + ".")
    return final_temp, desc2
