# used libraries
import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv

# look for .env file
load_dotenv("C:/Users/pavli/PycharmProjects/PORTFOLIO/.env.txt")

# Twillio authentication data
account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_TOKEN")

# data for Open Weather Map API
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
API_KEY = os.getenv("OWM_KEY")

# location coordinates
LAT = os.getenv("MY_LAT")
LNG = os.getenv("MY_LNG")

# parameters required by API
parameters = {
    "lat": LAT,
    "lon": LNG,
    "appid": API_KEY,
    "units": "metric",
    "exclude": "current,minutely,daily"
}

# get weather data from Open Weather Map
response = requests.get(url=OWM_Endpoint, params=parameters)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

# will_rain default value
will_rain = False

# check if there is any hour with codes for rain conditions
for hour in weather_slice:
    condition_code = hour["weather"][0]["id"]
    if condition_code < 700:
        will_rain = True

# send sms alert if it will rain
if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to="+385997580389",
        from_="+17069899587",
        body="It's going to rain today. Remember to bring an umbrella!")
    print(message.status)
