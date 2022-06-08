# used libraries
import datetime as dt
import pandas as pd
import random
import smtplib
import os
from dotenv import load_dotenv

# look for .env file
load_dotenv("C:/Users/pavli/PycharmProjects/PORTFOLIO/.env.txt")

# email log in data
MY_EMAIL = os.getenv("NOBODY_GMAIL_USER")
MY_PASSWORD = os.getenv("NOBODY_GMAIL_PASS")

FIRST_LETTER = 1  # number in the name of the first letter template
LAST_LETTER = 3  # number in the name of the last letter template
PLACEHOLDER = "[NAME]"  # value that needs to be replaced in letter templates

TODAY = dt.datetime.now().date()  # today's date
birthday_data = pd.read_csv("birthdays.csv")  # read file with list of birthdays

for name in birthday_data["name"]:  # go through the list of birthdays
    month = int(birthday_data['month'][birthday_data['name'] == name])  # get month of birth
    day = int(birthday_data['day'][birthday_data['name'] == name])  # get day of birth

    if TODAY.month == month and TODAY.day == day:  # check if it's person's birthday today
        letter_index = random.randint(FIRST_LETTER, LAST_LETTER)  # choose random letter template
        with open(f"./letter_templates/letter_{letter_index}.txt") as letter_template:  # open chosen letter template
            letter_contents = letter_template.read()  # read chosen letter template
            new_letter = letter_contents.replace(PLACEHOLDER, name)  # replace placeholder with the persons name

        # send birthday wishes over email
        email = str(birthday_data['email'][birthday_data['name'] == name])  # email of the person
        with smtplib.SMTP("smtp.gmail.com") as connection:  # connect to gmail server
            connection.starttls()  # make connection secure
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)  # log in to gmail
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=email,
                                msg=f"Subject:Happy Birthday\n\n{new_letter}")
