# used libraries
import requests
import os
from dotenv import load_dotenv

load_dotenv("C:/Users/pavli/PycharmProjects/PORTFOLIO/.env.txt")  # look for .env file

PRICES_Endpoint = "https://api.sheety.co/b9da1df6bf4a5adeefdf8967977e8b83/flightDeals/prices"  # link to Sheety table
bearer_headers = {"Authorization": os.getenv("SHEETY_AUTH")}  # authorization for Sheety table


class DataManager:
    """Models Sheety table manager"""

    def __init__(self):
        response = requests.get(url=PRICES_Endpoint, headers=bearer_headers)  # get prices from the table
        self.sheet_data = response.json()["prices"]

    def update_sheet_dict(self):
        """Updates IATA codes in Sheety table"""

        for n in range(2, len(self.sheet_data) + 2):
            update_endpoint = f"{PRICES_Endpoint}/{n}"
            body = {"price": {"iataCode": self.sheet_data[n-2]["iataCode"]}}
            requests.put(url=update_endpoint, json=body, headers=bearer_headers)
