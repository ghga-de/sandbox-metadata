import sys
import yaml
import requests


PATH = "http://localhost:8000/openapi.json"


if len(sys.argv) > 1:
    PATH=sys.argv[1]

response = requests.get(PATH)
json_data = response.json()
print(yaml.dump(json_data))
