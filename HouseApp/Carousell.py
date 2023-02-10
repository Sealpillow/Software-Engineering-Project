import requests
from bs4 import BeautifulSoup


#  https://www.dataquest.io/blog/python-api-tutorial/

area = "choa chu kang"
str = area.replace(" ", "%20")
addr = f"https://www.carousell.sg/categories/property-102/property-for-sale-230/hdb-1583/?addRecent=true&canChangeKeyword=true&includeSuggestions=true&search={str}&searchId=Mwp-LU"
response = requests.get(addr)
soup = BeautifulSoup(response.text, 'html.parser')
print(response.status_code)

for data in soup.find_all("div",{"class":"D_xZ M_rj"}):  # all listing url can be found under D_r_ D_x_-> D_xH
    print(data.a["href"])
    response2 = requests.get("https://www.carousell.sg"+data.a["href"])
    soup2 = BeautifulSoup(response2.text,"html.parser")
    for img in soup2.find_all("img",{"class":"D_vG M_pj D_vC M_pg D_aJt M_auF"}):
        print(img["src"])
    price = data.find_next("div",{"class":"D_yI M_rR"})  # price section
    print(price.text)  # get the text value
    title = data.find_next("p")  # next p tag which contains the address/title?
    print(title.text)
    #for features in data.find_all("div",{"class":"D_yP M_rY"}):  # whole feature bar
        # for feature in features.find_all("div",{"class":"D_yR M_sa"}):  # in each feature section in feature bar
    numList = [num.text for num in data.find_all("span",{"class":"D_uc M_lR D_rN M_lF D_ue M_lS D_uh M_lV D_uj M_lX D_un M_mb D_up M_me D_ut"})]
    bedroom = numList[0]
    bathroom = numList[1]
    pricePSF = numList[2]
    area = numList[3]
    # select the variable span class -> text value
    print(numList)

