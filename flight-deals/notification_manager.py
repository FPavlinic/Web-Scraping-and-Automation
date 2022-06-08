# used libraries
from twilio.rest import Client
import requests
import smtplib
from data_manager import bearer_headers
import os
from dotenv import load_dotenv

load_dotenv("C:/Users/pavli/PycharmProjects/PORTFOLIO/.env.txt")  # look for .env file

account_sid = os.getenv("TWILIO_SID")  # Twilio API acc SID
auth_token = os.getenv("TWILIO_TOKEN")  # Twilio API auth token

MY_NUMBER = os.getenv("PHONE_NUM")  # mobile phone number to send sms to
MY_EMAIL = os.getenv("NOBODY_GMAIL_USER")  # user to log in to email
MY_PASSWORD = os.getenv("NOBODY_GMAIL_PASS")  # password to log in to email


USERS_Endpoint = "https://api.sheety.co/b9da1df6bf4a5adeefdf8967977e8b83/flightDeals/users"  # url to Sheety table with user emails


class NotificationManager:
    """Models notification sender"""

    def __init__(self):
        pass

    def compare_prices(self, sheet_price, flight_price):
        """Compares prices in Sheety table with flight prices"""

        if flight_price < sheet_price:
            return True
        else:
            return False

    def send_sms(self, notification):
        """Sends sms notification with flight info"""

        client = Client(account_sid, auth_token)
        client.messages.create(to=MY_NUMBER,
                               from_="+17069899587",
                               body=notification)

    def send_mail(self, notification, flight_data):
        """Sends email notification with flight info"""

        response = requests.get(url=USERS_Endpoint, headers=bearer_headers)
        data = response.json()["users"]

        # create link to take user directly to the flight
        home_city = flight_data.departure_city.replace(" ", "-").lower()
        dst_city = flight_data.arrival_city.replace(" ", "-").lower()
        home_country = flight_data.departure_country.replace(" ", "-").lower()
        dst_country = flight_data.arrival_country.replace(" ", "-").lower()
        from_date = flight_data.departure_time.split("T")[0]
        to_date = flight_data.return_time.split("T")[0]
        link = f"https://www.kiwi.com/en/search/results/{home_city}-{home_country}/{dst_city}-{dst_country}/{from_date}/{to_date}?stopNumber=2%7Etrue&sortBy=price"
        # missing name of the State if country is USA for link to be fully functional

        # go through all emails in the list of users and send notification
        for n in range(len(data)):
            email = data[n]["email"]
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{notification}\n{link}"
                )
