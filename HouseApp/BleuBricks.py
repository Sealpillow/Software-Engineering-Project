import requests
import json
from bs4 import BeautifulSoup
import re
import generateBleuBricksLink
import webbrowser
#  https://www.dataquest.io/blog/python-api-tutorial/
# https://bobbyhadz.com/blog/python-remove-all-non-numeric-characters-from-string

def main(location, flatType, bed, bath, minPrice, maxPrice, minArea, maxArea):
    listing = []

    for region in location:
        pageNum = 0
        hasPage = True
        while hasPage:
            pageNum += 1
            link = generateBleuBricksLink.main(region, flatType, bed, bath, minPrice, maxPrice, minArea, maxArea,pageNum)
            # issue with this is that input location, have a set of list
            addr = f"https://www.bleubricks.com/listings/?sort=newest&search_status=61&search_neighborhood=d23_dairy_farm__bukit_panjang__choa_chu_kang&search_type=0&search_baths=0&search_price_min=&search_price_max="
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            # print(response.status_code)

            # region = [data.text for data in soup.find("select", {"name": "search_neighborhood"}).find_all("option")]
            # print(region)
            if soup.find("h2",{"class":"pxp-content-side-h2"}) is not None:
                hasPage = False
                continue
            websiteimg = "https://www.bleubricks.com/wp-content/uploads/2021/06/Bleubricks-by-PLB-Logo-Official-Recovered-01.png"
            for data in soup.find_all("div", {"class": "col-sm-12 col-md-6 col-xl-4"}):

                link = data.a["href"]
                # print(link)
                # webbrowser.open("https://www.bleubricks.com" + link)
                pic = data.find_next("div", {"class": "carousel-item"})  # just find 1 image
                # print(pic["style"])
                addr = data.find_next("div", {"class": "pxp-results-card-2-details-title"})
                feature = data.find_next("div", {"class": "pxp-results-card-2-features"})
                # print(' '.join(feature.text.split()))
                info = ' '.join(feature.text.split()).split("|")
                # print(info)
                price = data.find_next("div", {"class": "pxp-results-card-2-details-price"})
                price = price.text.replace(" ","").replace("\n","")
                price = price[0] + re.sub(r'[^0-9,]', '', price[1:])
                listing.append([link,pic["style"][22:-2],info[2],info[0],info[1],price,addr.text,websiteimg])
    return listing

if __name__ == "__main__":
    main()


