import requests
import json



response = requests.get(
    f"https://d2ssns4w4hvcti.cloudfront.net/systems/9748c3d9-3442-48cc-a8a6-40ec456beecb",
    headers={"X-Api-Key": "c0f729ac225ae545358ac0b0dbaea776"}
)

print(response.text)