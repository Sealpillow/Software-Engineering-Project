
def main(inputLocation,inputFlatType,inputBed,inputBath,inputMinPrice,inputMaxPrice,inputMinArea,inputMaxArea):
    locationList = ["Ang Mo Kio", "Bedok", "Bishan", "Bukit Batok", "Bukit Merah",
                  "Bukit Panjang", "Bukit Timah", "Central Area", "Choa Chu Kang",
                  "Clementi", "Geylang", "Hougang", "Jurong East", "Jurong West",
                  "Kallang/Whampoa", "Lim Chu Kang", "Marine Parade", "Pasir Ris",
                  "Punggol", "Queenstown", "Sengkang", "Serangoon", "Tampines", "Toa Payoh",
                  "Woodlands", "Yishun"]

    # if location not stated, e = "", it will include all locations, else append specific in increasing order
    location = ""
    for index,i in enumerate(inputLocation):
        location += "estate["+str(index)+"]="+i.replace(" ","%20")+"&"

    # 1 each only
    maxPrice = "max_price=" + inputMaxPrice + "&"
    maxArea = "max_size=" + inputMaxArea + "&"
    minPrice = "min_price=" + inputMinPrice + "&"
    minArea = "min_size=" + inputMinArea + "&"

    # if bath no stated, bh = "", else multiple statements in increasing order
    # nbath[0]=2&nbath[1]=3&
    numBath = ""
    for index,i in enumerate(inputBath):
        numBath += "nbath["+str(index)+"]="+i+"&"

    # if bath no stated, bh = "", else multiple statements in increasing order
    # nbed[0]=3&nbed[1]=4&
    numBed = ""
    for index,i in enumerate(inputBed):
        numBed += "nbed["+str(index)+"]="+i+"&"

    base = "https://clickproperty.sg/property-for-sale?actfilter=1&category_id[0]=3&" + location + "filterpress=0&isusefilter=1&keyword=&listviewtype=1&" + maxPrice + "max_properties=0&"+ maxArea + minPrice + minArea + numBath + numBed + "orderby=&ordertype=&ourl=/property-for-sale&property_type=1&uid=0"
    # print(base)
    return base

if __name__ == "__main__":
    main()
