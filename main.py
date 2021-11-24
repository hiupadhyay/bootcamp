from flask import Flask
from flask import request
import os
import requests
import json
import pyjokes


app = Flask('bootcamp')

# NOTE: EVERYTHING in this file is publically viewable. If you want to use private information (like private keys/passwords) in your application, please put them in a new .env file, and reference them like shown below.

# gets and prints TWILIO_ACCOUNT_SID value from .env file
# print(os.getenv("TWILIO_ACCOUNT_SID"))

@app.route('/sms', methods=['GET', 'POST'])
def sms():
  choice = request.form.get('Body')
  if choice=="cricket":
    return resp("Score is 250 +")
  elif choice=="hi" or choice=="hello" or choice=="tere" or choice=="namaste" or choice=="ola":
    return resp("""Welcome Amigos,Reply with Option  
  1) Joke
  2) Weather
  3) Cricket Score
  4) Quote of the day
  5) Current Location""")
  elif choice=="1":
   return resp(fetchLocation())
  elif choice=="5":
   return resp(fetchJoke())
  else:
    return resp("Invalid Choice....")
    


def resp(msg):
  return """<?xml version="1.0" encoding="UTF-8"?>
  <Response>
    <Message>"""+msg+"""</Message>
  </Response>"""

def fetchLocation():
  response = requests.get("http://api.open-notify.org/iss-now.json")
  response = response.json()
  print(response['iss_position'])
  return "latitude :"+response['iss_position']['latitude'] + " longitude: "+response['iss_position']['longitude']

def fetchJoke():
  return pyjokes.get_joke()

  


app.run(debug=True, host='0.0.0.0', port=8080)
