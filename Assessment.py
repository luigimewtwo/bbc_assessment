import requests

response = requests.get("https://d2ssns4w4hvcti.cloudfront.net/status",
                        headers={"X-API-Key": "c0f729ac225ae545358ac0b0dbaea776"}
                        )
print (response.text)