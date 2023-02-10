import requests
from bs4 import BeautifulSoup
import webbrowser

ListOfTown = ["Ang Mo Kio","Bedok","Bishan","Bukit Batok","Bukit Merah",
              "Bukit Panjang","Bukit Timah","Central Area","Choa Chu Kang",
              "Clementi","Geylang","Hougang","Jurong East","Jurong West",
              "Kallang/Whampoa","Lim Chu Kang","Marine Parade","Pasir Ris",
              "Punggol","Queenstown","Sengkang","Serangoon","Tampines","Toa Payoh",
              "Woodlands","Yishun"]



def main():
    listing = []
    area = "choa chu kang"
    str = area.replace(" ", "%20")

    addr = f"https://clickproperty.sg/property-for-sale?actfilter=1&category_id[0]=3&estate[0]={str}&filterpress=0&isusefilter=1&keyword=&listviewtype=1&max_price=&max_properties=0&max_size=&min_price=&min_size=&orderby=&ordertype=&ourl=/property-for-sale&property_type=1&uid=0"
    response = requests.get(addr)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(response.status_code)
    websiteimg = "https://cpsg.oss-ap-southeast-1.aliyuncs.com/img/logo/newt-long-gw-261-47-logo-compressor.png"
    for data in soup.find_all("li", {"class": "span12 listbox"}):  # all listing url can be found under D_r_ D_x_-> D_xH
        desc = data.find_next("div", {"class": "property-desc"})
        link = data.find_next("a", {"class": "property_mark_a"})
        img = data.find_next("img", {"class": "ospitem-imgborder lazyload lpiclass"})
        floorsize = data.find_next("span", {"itemprop": "floorSize"})
        numBed = data.find_next("span", {"itemprop": "numberOfBedrooms"})
        numBath = data.find_next("span", {"itemprop": "numberOfBathroomsTotal"})
        price = data.find_next("span", {"class": "listprice"})
        addr = data.find_next("div",{"style":"margin-bottom: 5px"})
        # print(link["href"])  # https://clickproperty.sg + link["href"]
        # print(img["smp"])
        # print(floorsize.text)
        # print(numBed.text)
        # print(numBath.text)
        # print(price)
        # webbrowser.open("https://clickproperty.sg" + link["href"])

        listing.append(["https://clickproperty.sg"+link["href"],img["smp"],floorsize.text,numBed.text,numBath.text,price.text,addr.text,websiteimg])
    return listing

if __name__ == "__main__":
    main()