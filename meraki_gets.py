import requests
import json

URL = "https://api.meraki.com/api/v0"
HEADERS = {
    "Content-Type": "application/json", 
    "X-Cisco-Meraki-API-Key": "6bec40cf957de430a6f1f2baa056b99a4fac9ea0", 
}

response = requests.get(
    URL + "/organizations", headers=HEADERS 
)

print(json.dumps(response.json(), indent=4))