from flask import Flask
from flask import request
import os

app = Flask('bootcamp')

# NOTE: EVERYTHING in this file is publically viewable. If you want to use private information (like private keys/passwords) in your application, please put them in a new .env file, and reference them like shown below.

# gets and prints TWILIO_ACCOUNT_SID value from .env file
# print(os.getenv("TWILIO_ACCOUNT_SID"))

@app.route('/sms', methods=['GET', 'POST'])
def sms():
  choice = request.form.get('Body')
  if choice=="cricket":
    return resp("Score is 250 +")
  else:
    return resp("")
    


def resp(msg):
  return """<?xml version="1.0" encoding="UTF-8"?>
  <Response>
    <Message>"""+msg+"""</Message>
  </Response>"""

app.run(debug=True, host='0.0.0.0', port=8080)
