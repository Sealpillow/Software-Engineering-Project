import requests
from bs4 import BeautifulSoup
import generateDirectHomeLink
# https://www.directhome.com.sg/listings?utf8=%E2%9C%93&q%5Blisting_type_eq%5D=1&q%5Bproperty_type_eq%5D=1&q%5B" + f + "name_or_description_or_address_cont%5D=&q%5B" + e + minPrice + maxPrice + numBed + numBath +"psf_gteq%5D=&q%5Bpsf_lteq%5D=&q%5Bland_area_gteq%5D=&q%5Bland_area_lteq%5D=&q%5B" +minfloor +maxfloor


def main(location, flatType, bed, bath, minPrice, maxPrice, minArea, maxArea):
    """
    This main function is to call generateDirectHomeLink.main() which generate link(s) for web scrapping

    Arg
        location (list): contain list of location option
        flatType (list): contain list of room option
        bed (list): contain list of bed option
        bath (list): contain list of bath option
        minPrice (str): contain min price input
        maxPrice (str): contain max price input
        minArea (str): contain min area input
        maxArea (str): contain max area input

    Returns:
        list: The all the listing information extracted from web scrapping
    """
    listing = []
    pageNum = 0
    hasPage = True
    while hasPage:
        pageNum += 1
        link = generateDirectHomeLink.main(location, flatType, bed, bath, minPrice, maxPrice, minArea, maxArea, pageNum)
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(response.status_code)
        websiteimg = "https://www.directhome.com.sg/assets/logo-new-f9d3c1a46c0edfb82895c5ab023fcc3ad89144b5bebb476b4aa41d1d827973f4.png"
        # indication that is end of page,
        if soup.find("div", {"class": "col-md-4 offset-md-4 col-xs-10 offset-xs-1"}) is not None:
            hasPage = False
            continue
        for data in soup.find_all("article", {"class": "product-classic product-classic-2"}):
            link = data.a["href"]
            # webbrowser.open("https://www.directhome.com.sg" + link)
            addr = data.find_next("h4", {"class": "product-classic-title"})
            addr = addr.text.split('\n')[2][4:]
            if addr is not None:
                addr = addr.replace("\'", " ")
                addr = addr.replace("\'s", " s") # incase there are strings that contain 's
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
            price = data.find_next("div", {"class": "product-classic-price"})
            price = price.text.replace(" ", "").replace("\n", "")
            pindex = price.find("(")
            if pindex > 0:
                price = price[:pindex]
            # print(price)
            img = data.find_next("img", {"class": "image_listing"})
            # print(image["src"])
            if img is None:
                image = "-"
            else:
                image = img["src"]
            listing.append(["https://www.directhome.com.sg" + link, image, info[3], info[1], info[2], price, addr, websiteimg])
    return listing
