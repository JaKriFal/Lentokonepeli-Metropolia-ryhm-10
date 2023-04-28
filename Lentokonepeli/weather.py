
from pip._vendor import requests


def Get_weather(player_location):
    city = player_location.split()[0]
    weather_url = "https://api.openweathermap.org/data/2.5/weather?q=" + \
        city + "&lang=fi&APPID=7c449d15551f18e130e9229fa2887cc3"
    response = requests.get(weather_url).json()
    if "main" in response and "temp" in response["main"]:
        temperature = response["main"]["temp"]
        final_temp = round(int(temperature) - 273.15, 2)
    else:
        final_temp = None
    if "weather" in response and response["weather"]:
        desc2 = response["weather"][0]["description"]
    else:
        desc2 = None
    if final_temp is not None and desc2 is not None:
        print("Sää " + city + " on " + str(final_temp) +
              " astetta ja " + desc2 + ".")
    else:
        print("Virhe haettaessa säätietoja kaupungista " + city + ".")
    return
