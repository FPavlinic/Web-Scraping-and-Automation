# used libraries
import requests
from datetime import datetime
import smtplib
import time
import os
from dotenv import load_dotenv

# look for .env file
load_dotenv("C:/Users/pavli/PycharmProjects/PORTFOLIO/.env.txt")

# location data
MY_LAT = 45.815010
MY_LNG = 15.981919

# log in to email data
MY_EMAIL = os.getenv("NOBODY_GMAIL_USER")
MY_PASSWORD = os.getenv("NOBODY_GMAIL_PASS")


def is_iss_overhead():
    """Checks if ISS is above the predefined location"""

    # get ISS data using API
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    # extract location data
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # check if ISS position is within +/-5 degrees of the predefined position
    if abs(MY_LAT - iss_latitude) < 5 and abs(MY_LNG - iss_longitude) < 5:
        return True


def is_night():
    """Checks if it's night at the predefined location"""

    # predefined location data
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0,
    }

    # use API to get sunrise and sunset data
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    # extract sunrise and sunset times
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour

    # check if current time is between sunset and sunrise --> night
    if time_now >= sunset or time_now <= sunrise:
        return True


def send_mail():
    """Sends email notification about ISS location"""

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=MY_EMAIL,
                            msg="Subject:Look up\n\nThe ISS is above your head.")


notify_me = True

# send notification if iss above predefined location and it's night
while notify_me:
    if is_iss_overhead() and is_night():
        send_mail()
        notify_me = False
    time.sleep(60)  # wait 60 seconds if above condition isn't met




