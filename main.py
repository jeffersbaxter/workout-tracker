import os

import requests
from datetime import datetime

APP_ID = os.environ.get("NUTRITIONIX_ID")
APP_KEY = os.environ.get("NUTRITIONIX_KEY")

exercise_params = {
    "query": "bicep curl lifted 10 sets of 10 reps",
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

# GET
# sheets_url = ""
#
# res = requests.get(url=sheets_url)
# res.raise_for_status()
# print(res.json())

today = datetime.now()
date = today.strftime("%Y%m%d")

post_body = {
    "workout": {
        "date": date,
        "time": today.strftime("%H:%M:%S"),
        "exercise": exercise,
        "duration": duration,
        "calories": calories
    }
}

post_sheets_url = os.environ.get("SHEETY_POST")

post_res = requests.post(url=post_sheets_url, json=post_body)
post_res.raise_for_status()
print(post_res.text)


