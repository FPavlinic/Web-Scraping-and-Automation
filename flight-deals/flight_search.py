# used libraries
import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv("C:/Users/pavli/PycharmProjects/PORTFOLIO/.env.txt")  # look for .env file

TEQUILA_Endpoint = "https://tequila-api.kiwi.com"  # link to Tequila API used for flights search
TEQUILA_API_KEY = {"apikey": os.getenv("API_TEQUILA_KEY")}  # key to use API

ORIGIN_CITY_CODE = "ZAG"  # IATA code of origin city
TODAY = datetime.now().date()  # get todays date
START_DATE = (TODAY + timedelta(days=1)).strftime("%d/%m/%Y")  # start date of flight search
END_DATE = (TODAY + timedelta(days=180)).strftime("%d/%m/%Y")  # end date of flight search


class FlightSearch:
    """Models flight researcher"""

    def __init__(self, sheet_data):
        self.data = sheet_data

    def find_iata_code(self, city_name):
        """Finds IATA codes by city name"""

        location_parameters = {
            "term": city_name,
            "locale": "en-US",
            "location_types": "city"
        }
        response = requests.get(url=f"{TEQUILA_Endpoint}/locations/query",
                                params=location_parameters,
                                headers=TEQUILA_API_KEY)
        data = response.json()
        return data["locations"][0]["code"]

    def find_flights(self,
                     fly_to,
                     max_stopovers,
                     fly_from=ORIGIN_CITY_CODE,
                     date_from=START_DATE,
                     date_to=END_DATE,
                     nights_in_dst_from=7,
                     nights_in_dst_to=28,
                     flight_type="round",
                     currency="USD",
                     locale="en",
                     limit=1):
        """Finds flights using below listed flight parameters"""

        flight_parameters = {
            "fly_from": fly_from,
            "fly_to": fly_to,
            "date_from": date_from,
            "date_to": date_to,
            "max_stopovers": max_stopovers,
            "nights_in_dst_from": nights_in_dst_from,
            "nights_in_dst_to": nights_in_dst_to,
            "flight_type": flight_type,
            "curr": currency,
            "locale": locale,
            "limit": limit
        }
        response = requests.get(url=f"{TEQUILA_Endpoint}/v2/search",
                                params=flight_parameters,
                                headers=TEQUILA_API_KEY)

        # print message if no flights are found
        try:
            data = response.json()['data'][0]
        except IndexError:
            if max_stopovers > 0:
                print(f"No available flights from {fly_from} to {fly_to}.")
            return False
        else:
            return data
