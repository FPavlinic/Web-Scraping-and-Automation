# used libraries
import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv

# constant (stock ticker)
STOCK_NAME = "TSLA"

# look for .env file
load_dotenv("C:/Users/pavli/PycharmProjects/PORTFOLIO/.env.txt")

# Alpha Vantage API data
AV_Endpoint = "https://www.alphavantage.co/query"
AV_API_KEY = os.getenv("API_AV_KEY")
AV_parameters = {
    "function": "Time_Series_Daily",
    "symbol": STOCK_NAME,
    "outputsize": "compact",
    "apikey": AV_API_KEY
}
# News API data
NEWS_Endpoint = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.getenv("API_NEWS_KEY")
NEWS_parameters = {
    "apiKey": NEWS_API_KEY,
    "q": STOCK_NAME,
    "searchIn": "title,description",
    "sortBy": "publishedAt",
    "language": "en"
}

# Twilio API data
account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_TOKEN")

# get stock data
stock_response = requests.get(url=AV_Endpoint, params=AV_parameters)
stock_data = stock_response.json()["Time Series (Daily)"]
stock_data_list = [value for (key, value) in stock_data.items()]

yesterday_data = stock_data_list[0]  # yesterdays data
dbf_yesterday_data = stock_data_list[1]  # data of the day before yesterday

# closing prices
price_yesterday = float(yesterday_data['4. close'])
price_dbf_yesterday = float(dbf_yesterday_data['4. close'])

# percentage of price difference
percent_diff = round((abs(price_yesterday - price_dbf_yesterday) / price_dbf_yesterday) * 100)

# check direction of price movement
if price_dbf_yesterday > price_yesterday:
    direction = "🔻"
else:
    direction = "🔺"

# check if difference in price is greater than 5
if percent_diff >= 5:
    news_response = requests.get(url=NEWS_Endpoint, params=NEWS_parameters)
    news_data = news_response.json()

    # get first few relevant articles (titles and descriptions)
    news = ""
    for n in range(3):
        title = news_data["articles"][n]["title"]
        description = news_data["articles"][n]["description"]
        news += f"\nHeadline: {title}\nBrief: {description}\n"

    # send sms with the stock price and the news
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to="+385997580389",
        from_="+17069899587",
        body=f"{STOCK_NAME}: {direction}{percent_diff}%{news}")
    print(message.status)


