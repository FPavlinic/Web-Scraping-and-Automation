# used libraries
from rental_data import RentalListings
from form_filling_bot import FormFiller

# shortened rentals url
ZILLOW_LINK = "https://bit.ly/3M3zpNv"

# google forms url
FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSc0k1jdZkzMuQbteyuuLkJuRmBrgbWj8OVZ8vtBU5aSooTxdA/viewform?usp=sf_link"

# HTTP header used while sending requests
HTTP_HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
    "Accept-Language": "en-US,en;q=0.5"
}

data = RentalListings(ZILLOW_LINK, HTTP_HEADER)  # create an object to get rental data
links = data.find_links()  # store links to rentals
prices = data.find_prices()  # store prices of rentals
addresses = data.find_addresses()  # store addresses of rentals
form = FormFiller(FORM_LINK, links, prices, addresses)  # create an object to fill form
