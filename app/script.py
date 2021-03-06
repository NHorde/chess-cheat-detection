import requests
import json
import os

import pandas as pd

from dotenv import load_dotenv
load_dotenv()

url = "https://www.lichess.org/api/games/user/NHorde"

headers = {
            "accept": "application/x-ndjson"
        }

params = {
    "max": 10,
    "opening": "true"
}

LICHESS_API_TOKEN = os.getenv("LICHESS_API_TOKEN")

r = requests.get(url = url,
                         params=params,
                         headers=headers)

r_text = r.content.decode("utf-8")

response = [json.loads(s) for s in r_text.split("\n")[:-1]]

def parser(row):
    return pd.json_normalize(response[row])

# Initialize
df = parser(row=0)

for i in range(len(response)-1):
    df = df.append(parser(row=i+1), ignore_index=False)

df.head(2)

df.to_csv("sample_game.csv")