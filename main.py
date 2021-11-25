from flask import Flask
from flask import request
import requests
import pyjokes
from geopy.geocoders import Nominatim
import geocoder
import yfinance as yf

app = Flask('bootcamp')

# NOTE: EVERYTHING in this file is publically viewable. If you want to use private information (like private keys/passwords) in your application, please put them in a new .env file, and reference them like shown below.

# gets and prints TWILIO_ACCOUNT_SID value from .env file
# print(os.getenv("TWILIO_ACCOUNT_SID"))
main_menu = """Welcome Amigos,Reply with Option  
  1) Joke
  2) Stock Prize
  3) What is my Address
  4) Main Menu"""

stock_prize = "Enter Ticker Symbol"


@app.route('/sms', methods=['GET', 'POST'])
def sms():
    choice = request.form.get('Body')
    if choice == "cricket":
        return resp("Score is 250 +")
    elif choice == "hi" or choice == "hello" or choice == "tere" or choice == "namaste" or choice == "ola":
        return resp(main_menu)
    elif choice == "3":
        return resp(fetchLocation())
    elif choice == "1":
        return resp(fetchJoke())
    elif choice == "2":
        return resp(stock_prize)
    elif choice == "4":
        return resp(main_menu)
    else:
        if validTicker(choice) == "0":
            return resp(stockprize(choice))
        else:
            return resp("""try again..
        """ + main_menu + """
         """)


def resp(msg):
    return """<?xml version="1.0" encoding="UTF-8"?>
  <Response>
    <Message>""" + msg + """</Message>
  </Response>"""


def validTicker(ticker):
    print(yf.Ticker(ticker))
    try:
        yf.Ticker(ticker)
        return "0"
    except:
        return "1"


def stockprize(ticker):
    ticker = yf.Ticker(ticker).history(period='1d')
    return str(ticker['Close'][0])


def fetchLocation():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    response = response.json()
    Latitude = response['iss_position']['latitude']
    Longitude = response['iss_position']['longitude']
    return str(fetchAddress(Latitude, Longitude))


def fetchJoke():
    return pyjokes.get_joke()


def fetchAddress(latitude, longitude):
    geolocator = Nominatim(user_agent="geoapiExercises")
    response = requests.get("http://api.open-notify.org/iss-now.json")
    response = response.json()
    g = geocoder.ip('me')
    print(g.latlng)
    Latitude = response['iss_position']['latitude']
    Longitude = response['iss_position']['longitude']
    print(Latitude + "," + Longitude)
    location = geolocator.reverse("59.43855209686544" + "," +
                                  "24.763826879144023")
    print(location)
    address = location.raw['address']
    pairs = address.items()
    str = ""
    for key, value in pairs:
        str = str + " " + value + "\n"
    return str


app.run(debug=True, host='0.0.0.0', port=8080)
