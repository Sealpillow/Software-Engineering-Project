import requests
import json
from bs4 import BeautifulSoup

import webbrowser
#  https://www.dataquest.io/blog/python-api-tutorial/
# https://app.swaggerhub.com/apis/onemap-sg/new-onemap-api/1.0.4#/Authentication%20Service%20(POST)/getToken
# token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjk3MTUsInVzZXJfaWQiOjk3MTUsImVtYWlsIjoibHVhdGFuNjhAaG90bWFpbC5jb20iLCJmb3JldmVyIjpmYWxzZSwiaXNzIjoiaHR0cDpcL1wvb20yLmRmZS5vbmVtYXAuc2dcL2FwaVwvdjJcL3VzZXJcL3Nlc3Npb24iLCJpYXQiOjE2NzQyMjE0MzgsImV4cCI6MTY3NDY1MzQzOCwibmJmIjoxNjc0MjIxNDM4LCJqdGkiOiI1MjJlODRiOGZlODQ4ZDBkYzIwYzRkZGIzNmYxYTNlNSJ9.X6Rx9NCFaKoj2MPnrMp7DdoYX2NVh8QNg9MIjpzSaxI"
def jprint(obj):
    # create a formatted string of the Python JSON object
    # json.dumps() — Takes in a Python object, and converts (dumps) it to a string.
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

# If you want to read a json file -> json.loads() — Takes a JSON string, and converts (loads) it to a Python object.


# API
response = requests.get("https://data.gov.sg/api/action/datastore_search?resource_id=f1765b54-a209-4718-8d38-a39237f502b3&limit=100")
if response.status_code !=200:
    print("Api cant be found")
data = response.json()
print(data)
print(data["result"])
jprint(data["result"]["records"])
print(data["result"]["records"][0]["town"])

list4r = []
for flat in data["result"]["records"]:
    if flat["flat_type"] == "3 ROOM":
        list4r.append(flat)
jprint(list4r)


