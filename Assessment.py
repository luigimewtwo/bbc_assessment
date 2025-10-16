import requests
import json

response = requests.get("https://d2ssns4w4hvcti.cloudfront.net/systems",
                        headers={"X-API-Key": "c0f729ac225ae545358ac0b0dbaea776"}
                        )

data = response.json()

id_lines = [f" {item['id']}" for item in data if "id" in item]

with open("systems.txt", "a") as file:
    for  id in id_lines:
        file.write(id + "\n")