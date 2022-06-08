# used libraries
import os
from dotenv import load_dotenv
from bot import InternetSpeedTwitterBot

load_dotenv("C:/Users/pavli/PycharmProjects/PORTFOLIO/.env.txt")  # look for .env file

PROMISED_UP = 200  # internet provider promised upload
PROMISED_DOWN = 500  # internet provider promised download

# Twitter login data
TWITTER_EMAIL = os.getenv("TWITTER_USER")
TWITTER_PASSWORD = os.getenv("TWITTER_PASS")

# create bot
bot = InternetSpeedTwitterBot()

# get your internet speed
bot.get_internet_speed()

# log in to Twitter and post a complaint
bot.tweet_at_provider(TWITTER_EMAIL, TWITTER_PASSWORD, bot.up, bot.down, PROMISED_UP, PROMISED_DOWN)

