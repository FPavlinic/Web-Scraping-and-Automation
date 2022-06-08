# used libraries
from bot import InstaFollower
import os
from dotenv import load_dotenv

load_dotenv("C:/Users/pavli/PycharmProjects/PORTFOLIO/.env.txt")  # look for .env file

# Instagram login data
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USER")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASS")
FOLLOW_PROFILE = "buzzfeedtasty"


bot = InstaFollower()  # create bot
bot.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)  # log in to Instagram
bot.find_followers(FOLLOW_PROFILE)  # open predefined Instagram profile and follow its followers
