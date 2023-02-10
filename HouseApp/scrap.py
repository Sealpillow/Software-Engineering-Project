import requests
from bs4 import BeautifulSoup

addr = f"https://www.w3schools.com/w3css/tryw3css_templates_hotel.htm"
response = requests.get(addr)
soup = BeautifulSoup(response.text, 'html.parser')
print(response.status_code)
for img in soup.find_all("img"):
    print("https://www.w3schools.com"+img["src"])

