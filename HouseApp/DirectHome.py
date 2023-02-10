import requests
import json
from bs4 import BeautifulSoup

import webbrowser
#  https://www.dataquest.io/blog/python-api-tutorial/
# https://bobbyhadz.com/blog/python-remove-all-non-numeric-characters-from-string

def main():
    listing = []
    area = "yew tee"
    str = area.replace(" ", "+")
    addr = f"https://www.directhome.com.sg/listings?utf8=%E2%9C%93&q%5Blisting_type_eq%5D=1&q%5Bproperty_type_eq%5D=1&q%5Bproperty_subtype_id_in%5D%5B%5D=aa4b1aee-1300-4e4e-a1f8-d6bd5ab8eb6e&q%5Bproperty_subtype_id_in%5D%5B%5D=c978c00b-399c-4b4b-95a1-4842c96caa6d&q%5Bproperty_subtype_id_in%5D%5B%5D=a245ff94-fbb4-4a80-bfe6-77f6363492f0&q%5Bproperty_subtype_id_in%5D%5B%5D=5a097d03-7a7f-4739-a485-3d1bb0ef77ca&q%5Bproperty_subtype_id_in%5D%5B%5D=5d30dc25-35ce-4970-9459-4bbd919c58b1&q%5Bproperty_subtype_id_in%5D%5B%5D=d5d14f8c-9067-4f20-9900-ba6f29cbd6e7&q%5Bproperty_subtype_id_in%5D%5B%5D=740fab01-56ad-4ad4-afac-647e6316b015&q%5Bproperty_subtype_id_in%5D%5B%5D=61b1ee76-a689-41dd-bc2f-29ad2fbba31b&q%5Bproperty_subtype_id_in%5D%5B%5D=01c08e4a-ab93-4b29-958a-58cefb907686&q%5Bproperty_subtype_id_in%5D%5B%5D=86f7844e-8530-4866-a934-9b38bd430ba4&q%5Bproperty_subtype_id_in%5D%5B%5D=1eaee8f8-e5e7-4366-9754-39a10e87d29a&q%5Bproperty_subtype_id_in%5D%5B%5D=35ea7469-6423-4c78-aacc-ef2eddce5fd7&q%5Bname_or_description_or_address_cont%5D={str}&q%5Bprice_gteq%5D=&q%5Bprice_lteq%5D=&commit=Search&q%5Bpsf_gteq%5D=&q%5Bpsf_lteq%5D=&q%5Bland_area_gteq%5D=&q%5Bland_area_lteq%5D=&q%5Bfloor_area_gteq%5D=&q%5Bfloor_area_lteq%5D="

    response = requests.get(addr)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(response.status_code)
    websiteimg = "https://www.directhome.com.sg/assets/logo-new-f9d3c1a46c0edfb82895c5ab023fcc3ad89144b5bebb476b4aa41d1d827973f4.png"
    for data in soup.find_all("article", {"class": "product-classic product-classic-2"}):
        link = data.a["href"]
        # print(link)
        # webbrowser.open("https://www.directhome.com.sg" + link)
        addr = data.find_next("h4", {"class": "product-classic-title"})
        addr = addr.text.split('\n')[2][4:]
        # print(addr)
        # print(' '.join(addr.text.split()))
        info = []  # contains info of listing
        for ul in data.find_all("ul", {"class": "product-classic-list"}):
            for li in ul.find_all("li"):
                liList = li.find_all("span")
                # print(' '.join(liList[1].text.split()))  #
                info.append(' '.join(liList[1].text.split()))
            span = ul.find_all("span")
            # print(' '.join(span[7].text.split()))
            info.append(' '.join(span[7].text.split()))
        price = data.find_next("div",{"class": "product-classic-price"})
        price = price.text.replace(" ", "").replace("\n", "")
        pindex = price.find("(")
        if pindex > 0:
            price = price[:pindex]
        # print(price)
        image = data.find_next("img", {"class": "image_listing"})
        # print(image["src"])
        listing.append(["https://www.directhome.com.sg"+link,image["src"],info[3],info[1],info[2],price,addr,websiteimg])
    return listing


if __name__ == "__main__":
    main()

