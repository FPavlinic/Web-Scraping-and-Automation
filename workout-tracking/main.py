# used libraries
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# constants
GENDER = "male"
WEIGHT_KG = 98
HEIGHT_CM = 183
AGE = 25

# current date and time
DATE = datetime.now().strftime("%d/%m/%Y")
TIME = datetime.now().strftime("%H:%M:%S")

# look for .env file
load_dotenv("C:/Users/pavli/PycharmProjects/PORTFOLIO/.env.txt")

# Nutritionix API data
APP_ID = os.environ["NT_APP_ID"]
API_KEY = os.environ["NT_API_KEY"]
NUTRITIONIX_Endpoint = "https://trackapi.nutritionix.com"
exercise_endpoint = f"{NUTRITIONIX_Endpoint}/v2/natural/exercise"

# ask user about exercises he did (answer in natural language)
exercise_text = input("Tell me which exercise you did: ")

# API requested headers
headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

# API requested body
body = {
    "query": exercise_text.title(),
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

# get data from the API
response = requests.post(url=exercise_endpoint, json=body, headers=headers)
result = response.json()

# Endpoint to the exercise tracking table
sheety_endpoint = os.environ["SHEET_ENDPOINT"]

# Sheety requested headers
bearer_headers = {
    "Authorization": f"Bearer {os.environ['TOKEN']}"
}

# get exercise data for every exercise in results of the request
for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": DATE,
            "time": TIME,
            "exercise": exercise["name"].title(),
            "duration": round(exercise["duration_min"]),
            "calories": round(exercise["nf_calories"])
        }
    }
    # post exercise data to the table using Sheety
    response = requests.post(url=sheety_endpoint, json=sheet_inputs, headers=bearer_headers)
