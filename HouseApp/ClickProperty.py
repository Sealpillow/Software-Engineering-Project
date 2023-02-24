import requests
from bs4 import BeautifulSoup
import webbrowser
import generateClickPropertyLink


def main(location,flatType,bed,bath,minPrice,maxPrice,minArea,maxArea):
    listing = []
    link = generateClickPropertyLink.main(location,flatType,bed,bath,minPrice,maxPrice,minArea,maxArea)
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(response.status_code)
    websiteimg = "https://cpsg.oss-ap-southeast-1.aliyuncs.com/img/logo/newt-long-gw-261-47-logo-compressor.png"
    for data in soup.find_all("li", {"class": "span12 listbox"}):  # all listing url can be found under D_r_ D_x_-> D_xH
        # desc = data.find_next("div", {"class": "property-desc"})
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
