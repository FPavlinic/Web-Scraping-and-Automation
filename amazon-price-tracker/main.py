# used libraries
import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv


PRODUCT_URL = "https://amzn.to/3M77BI3"  # shortened url to tracked product
WANTED_PRICE = 200  # wanted price for tracked product

# look for .env file
load_dotenv("C:/Users/pavli/PycharmProjects/PORTFOLIO/.env.txt")

# email log in data
MY_EMAIL = os.getenv("NOBODY_GMAIL_USER")
MY_PASSWORD = os.getenv("NOBODY_GMAIL_PASS")

# email address to send an email to
MY_2_EMAIL = os.getenv("PF_GMAIL_USER")

# HTTP headers used while sending requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(url=PRODUCT_URL, headers=headers)  # send request to url
soup = BeautifulSoup(response.content, "html.parser")  # get html from url

product_name = soup.find(id="productTitle").getText().strip()  # extract product name from html
price = float(soup.find(class_="a-offscreen").getText().split("$")[1])  # extract product price from html

# message to send via email when lower condition is met
message = f"Subject:Amazon Price Alert!\n\n{product_name} is now ${price}\n{PRODUCT_URL}"

if price < WANTED_PRICE:
    with smtplib.SMTP("smtp.gmail.com") as connection:  # connect to gmail server
        connection.starttls()  # make connection secure
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)  # log in to gmail
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=MY_2_EMAIL,
                            msg=message.encode('utf8'))  # encode message to support all characters
