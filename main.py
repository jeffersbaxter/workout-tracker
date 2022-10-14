import os

import requests
from datetime import datetime

APP_ID = os.environ.get("NUTRITIONIX_ID")
if not APP_ID:
    raise Exception("app id not set for Nutritionix API")

APP_KEY = os.environ.get("NUTRITIONIX_KEY")
if not APP_KEY:
    raise Exception("app key not set for Nutritionix API")

SHEETY_AUTH = os.environ.get("SHEETY_AUTH")
if not SHEETY_AUTH:
    raise Exception("bearer token not set for Sheety API")

SHEETY_POST = os.environ.get("SHEETY_POST")
if not SHEETY_POST:
    raise Exception("POST endpoint not set for Sheety API")

workout_text = input("Describe your workout? ")

exercise_params = {
    "query": workout_text,
    "gender": "male",
    "weight_kg": 81.8,
    "height_cm": 187.96,
    "age": 32
}

headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY
}

exercise_url = "https://trackapi.nutritionix.com/v2/natural/exercise"

res = requests.post(url=exercise_url, json=exercise_params, headers=headers)
res.raise_for_status()

data = res.json()
exercises = data["exercises"]
exercise = exercises[0]["user_input"]
duration = exercises[0]["duration_min"]
calories = exercises[0]["nf_calories"]

today = datetime.now()
date = today.strftime("%m/%d/%Y")

post_body = {
    "workout": {
        "date": date,
        "time": today.strftime("%H:%M:%S"),
        "exercise": exercise,
        "duration": duration,
        "calories": calories
    }
}

post_headers = {
    "Authorization": SHEETY_AUTH
}

post_sheets_url = SHEETY_POST

post_res = requests.post(url=post_sheets_url, json=post_body, headers=post_headers)
post_res.raise_for_status()
print(post_res.text)


