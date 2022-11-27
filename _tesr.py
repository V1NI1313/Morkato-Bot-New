import requests
import json

url = "http://localhost:5500/desktop/Guilds/89897685"

headers = {'content-type': 'application/json'}
 
data = {
  "human": 94988334949943,
  "oni": 467839882768302,
  "hybrid": 383889292939,
  "separator": []
}
 
response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.json())