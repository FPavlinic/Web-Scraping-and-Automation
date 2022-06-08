# used libraries
import requests
from bs4 import BeautifulSoup
import json
import time


class RentalListings:
    """Models rental data researcher"""

    def __init__(self, link, http_header):
        # go to rentals url
        response = requests.get(url=link, headers=http_header)
        # wait to seem more human like
        time.sleep(3)
        # get html from the url
        results = response.text
        self.soup = BeautifulSoup(results, "html.parser")
        # get results from <script> variable stored in json form inside the html
        self.data = json.loads(str(self.soup.select_one("script[data-zrr-shared-data-key]")
                               .contents[0])
                               .strip("!<>-")
                               )

    def find_links(self):
        """Returns links to rentals"""

        links = [result["detailUrl"] for result in self.data["cat1"]["searchResults"]["listResults"]]

        # create list of rental links
        house_links = [
            link.replace(link, "https://www.zillow.com" + link)
            if not link.startswith("http")
            else link
            for link in links
        ]
        return house_links

    def find_prices(self):
        """Returns prices of rentals"""

        # create list of prices
        prices = [
            int(result["units"][0]["price"].strip("$").replace(",", "").strip("+"))
            if "units" in result
            else result["unformattedPrice"]
            for result in self.data["cat1"]["searchResults"]["listResults"]
        ]
        return prices

    def find_addresses(self):
        """Returns addresses of rentals"""

        # create list of addresses
        addresses = [
            result["address"]
            for result in self.data["cat1"]["searchResults"]["listResults"]
        ]
        return addresses




