import requests
from bs4 import BeautifulSoup

addr = "https://data.gov.sg/dataset/resale-flat-prices"
response = requests.get(addr)
soup = BeautifulSoup(response.text, 'html.parser')
print(response.status_code)
info = soup.find("div", {"class": "module-content"})
print(info)


