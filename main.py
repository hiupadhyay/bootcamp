from flask import Flask
from flask import request
import requests,json
import pyjokes
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup

app = Flask('bootcamp')

# NOTE: EVERYTHING in this file is publically viewable. If you want to use private information (like private keys/passwords) in your application, please put them in a new .env file, and reference them like shown below.

# gets and prints TWILIO_ACCOUNT_SID value from .env file
# print(os.getenv("TWILIO_ACCOUNT_SID"))
main_menu = """Welcome Amigos,Reply with Option  
  1) Joke
  2) Current Weather
  3) Quote of the day
  4) Current Location
  5) Main Menu"""
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


@app.route('/sms', methods=['GET', 'POST'])
def sms():
    choice = request.form.get('Body')
    if choice == "cricket":
        return resp("Score is 250 +")
    elif choice == "hi" or choice == "hello" or choice == "tere" or choice == "namaste" or choice == "ola":
        return resp(main_menu)
    elif choice == "4":
        return resp(fetchLocation())
    elif choice == "1":
        return resp(fetchJoke())
    elif choice == "2":
        return resp(fetchWeather())
    elif choice == "5":
        return resp(main_menu)
    else:
        return resp("""try again..
  """ + main_menu + """
    """)


def resp(msg):
    return """<?xml version="1.0" encoding="UTF-8"?>
  <Response>
    <Message>""" + msg + """</Message>
  </Response>"""


def fetchLocation():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    response = response.json()
    print(response['iss_position'])
    return "latitude :" + response['iss_position'][
        'latitude'] + " longitude: " + response['iss_position']['longitude']


def fetchJoke():
    return pyjokes.get_joke()


def fetchWeather():
    geolocator = Nominatim(user_agent="geoapiExercises")
    response = requests.get("http://api.open-notify.org/iss-now.json")
    response = response.json()
    Latitude = response['iss_position']['latitude']
    Longitude = response['iss_position']['longitude']
    print(Latitude + "," + Longitude)
    location = geolocator.reverse("59.43855209686544" + "," +
                                  "24.763826879144023")
    address = location.raw['address']
    city = address.get('city')
    return weather(city)


def weather(city):
  BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
  API_KEY="91b99c89ad821c042502bbe45675d759"
  URL = BASE_URL + "q=" + city + "&appid=" + API_KEY
  response = requests.get(URL)
  main = response.json()['main']
  temperature = main.get('temp')
  print(temperature)
  humidity = main.get('humidity')
  pressure = main.get('pressure')
  report = main.get('weather')
  print(main)
  return str(humidity)





app.run(debug=True, host='0.0.0.0', port=8080)
