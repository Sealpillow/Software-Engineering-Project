def main(inputLocation, inputFlatType, inputBed, inputBath, inputMinPrice, inputMaxPrice, inputMinArea, inputMaxArea,pageNum):
    """
    This function is to generate url for web scrapping based on inputs

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
        str: The url for web scrapping based on inputs
    """
    # https://www.directhome.com.sg/listings?utf8=%E2%9C%93&q[listing_type_eq]=1&q[property_type_eq]=1&q[property_subtype_id_in][]=a245ff94-fbb4-4a80-bfe6-77f6363492f0&q[property_subtype_id_in][]=5a097d03-7a7f-4739-a485-3d1bb0ef77ca&q[name_or_description_or_address_cont]=choa+chu+kang&q[estate_id_in][]=56e7f452-cb9d-4d3d-b7c8-9f4295e91f46&q[estate_id_in][]=09c4c3bd-1f8f-4544-b598-75dc527e62c0&q[price_gteq]=0&q[price_lteq]=12345567&q[bedrooms_in][]=2&q[bedrooms_in][]=3&q[bathrooms_in][]=2&q[bathrooms_in][]=3&q[psf_gteq]=&q[psf_lteq]=&q[land_area_gteq]=&q[land_area_lteq]=&q[floor_area_gteq]=500.0&q[floor_area_lteq]=&commit=Search&page=1
    # https://www.directhome.com.sg/listings?utf8=%E2%9C%93&q[listing_type_eq]=1&q[property_type_eq]=1&q[" + f + "name_or_description_or_address_cont]=&q[" + e + minPrice + maxPrice + numBed + numBath +"psf_gteq]=&q[psf_lteq]=&q[land_area_gteq]=&q[land_area_lteq]=&q[" +minfloor +maxfloor

    # multiply same str but diff value if multiple flat option chosen
    flatType = {"1 Room": "[property_subtype_id_in][]=aa4b1aee-1300-4e4e-a1f8-d6bd5ab8eb6e&q",
                "2 Room": "[property_subtype_id_in][]=c978c00b-399c-4b4b-95a1-4842c96caa6d&q",
                "3 Room": "[property_subtype_id_in][]=a245ff94-fbb4-4a80-bfe6-77f6363492f0&q",
                "4 Room": "[property_subtype_id_in][]=5a097d03-7a7f-4739-a485-3d1bb0ef77ca&q",
                "5 Room": "[property_subtype_id_in][]=5d30dc25-35ce-4970-9459-4bbd919c58b1&q"}

    # multiply same str but diff value if multiple estate option chosen
    locationList = {"Ang Mo Kio": "[estate_id_in][]=56e7f452-cb9d-4d3d-b7c8-9f4295e91f46&q",
                    "Bedok": "[estate_id_in][]=0c5982d8-e614-4b2f-a308-e19398445c1f&q",
                    "Bishan": "[estate_id_in][]=fde2df6b-7bcd-459d-ab54-e7b3576c85b2&q",
                    "Bukit Batok": "[estate_id_in][]=0cfd3919-90f1-449e-8629-eae72e0bf0ce&q",
                    "Bukit Merah": "[estate_id_in][]=472d9944-1e44-4e84-9686-ca5ef40fffcd&q",
                    "Bukit Panjang": "[estate_id_in][]=6a0e73ad-545a-4525-a0f5-008da07fddb9&q",
                    "Bukit Timah": "[estate_id_in][]=530adb55-e58d-4595-8091-dc31c792cfda&q",
                    "Central Area": "[estate_id_in][]=9b3ce37f-c08c-46f1-a550-7e0822bffa34&q",
                    "Choa Chu Kang": "[estate_id_in][]=09c4c3bd-1f8f-4544-b598-75dc527e62c0&q",
                    "Clementi": "[estate_id_in][]=ee42c0dc-0de6-4c9b-ac90-901e02ab5a71&q",
                    "Geylang": "[estate_id_in][]=22d660c6-3522-43b0-b75f-e74a53e9bcae&q",
                    "Hougang": "[estate_id_in][]=9dcf44f2-65f2-4de8-878f-c4dd99b1242a&q",
                    "Jurong East": "[estate_id_in][]=5640bee6-4c93-4250-b67f-2d1cd1143948&q",
                    "Jurong West": "[estate_id_in][]=fc1a8bfc-2011-4aba-91ab-fe0a1849c5e7&q",
                    "Kallang/Whampoa": "[estate_id_in][]=3461f9ba-2eb8-4dda-ada5-1a20c757a7b1&q",
                    "Lim Chu Kang": "[estate_id_in][]=bd6c288c-eb58-45a5-b367-08f4b9b99569&q",
                    "Marine Parade": "[estate_id_in][]=d460dadb-83ec-4f15-a225-c07cc0f5f246&q",
                    "Pasir Ris": "[estate_id_in][]=6f3e8ef6-ea5c-431f-9f7d-284dc2cda32d&q",
                    "Punggol": "[estate_id_in][]=e31bb373-6fb0-4253-9be3-a56ae477b04e&q",
                    "Queenstown": "[estate_id_in][]=c2380772-34e9-4e41-8747-a1d1eceb8a2b&q",
                    "Sembawang": "[estate_id_in][]=ee40d503-2371-43ed-81c8-a068dd636d7d&q",
                    "Sengkang": "[estate_id_in][]=4c0a5428-249f-42ba-94bd-edf1f88d27a3&q",
                    "Serangoon": "[estate_id_in][]=709538a0-7f92-40df-ba6c-4689af6e39e0&q",
                    "Tampines": "[estate_id_in][]=bedc9a3a-ab13-493d-8d11-144f9d14300b&q",
                    "Toa Payoh": "[estate_id_in][]=a85528cf-a152-4cb4-bcab-30cfdf6e8c15&q",
                    "Woodlands": "[estate_id_in][]=57f10ff9-d37f-4307-b011-92a55190f1ed&q",
                    "Yishun": "[estate_id_in][]=001cca85-a594-4a49-baf8-225a11bef4fa&q",
                    }

    # if room not stated, append all keys, else append specific
    room = ""
    for i in inputFlatType:
        room += flatType[i]

    # if location not stated, e = "", it will include all locations, else append specific in increasing order
    location = ""
    for i in inputLocation:
        location += locationList[i]

    # if bath no stated, bh = "", else multiple statements in increasing order

    numBed = ""
    for i in inputBed:
        numBed += "[bedrooms_in][]=" + i + "&q"

    # if bath no stated, bh = "", else multiple statements in increasing order
    numBath = ""
    for i in inputBath:
        numBath += "[bathrooms_in][]=" + i + "&q"

    # only have 1 each
    minPrice = "[price_gteq]=" + inputMinPrice + "&q"
    maxPrice = "[price_lteq]=" + inputMaxPrice + "&commit=Search&q"

    # only have 1 each
    minfloor = "[floor_area_gteq]=" + inputMinArea + "&q"
    maxfloor = "[floor_area_lteq]=" + inputMaxArea + "&"

    # consider copy multiple page, after end of last page-> interval server error

    base = "https://www.directhome.com.sg/listings?utf8=%E2%9C%93&q[listing_type_eq]=1&q[property_type_eq]=1&q" + room + "[name_or_description_or_address_cont]=&q" + location + minPrice + maxPrice + numBed + numBath + "[psf_gteq]=&q[psf_lteq]=&q[land_area_gteq]=&q[land_area_lteq]=&q" + minfloor + maxfloor + "commit=Search&page="+ str(pageNum)
    # print(base)
    return base


if __name__ == "__main__":
    main()
