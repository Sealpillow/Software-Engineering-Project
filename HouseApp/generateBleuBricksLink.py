def main(inputLocation, inputFlatType, inputBed, inputBath, inputMinPrice, inputMaxPrice, inputMinArea, inputMaxArea, pageNum):
    locationList = ["Ang Mo Kio",
                    "Bedok",
                    "Bishan",
                    "Bukit Batok",
                    "Bukit Merah",
                    "Bukit Panjang",
                    "Bukit Timah",
                    "Central Area",
                    "Choa Chu Kang",
                    "Clementi",
                    "Geylang",
                    "Hougang",
                    "Jurong East",
                    "Jurong West",
                    "Kallang/Whampoa",
                    "Lim Chu Kang",
                    "Marine Parade",
                    "Pasir Ris",
                    "Punggol",
                    "Queenstown",
                    "Sengkang",
                    "Serangoon",
                    "Tampines",
                    "Toa Payoh",
                    "Woodlands",
                    "Yishun"]
    locationList = {"All": "",
                    "D01 Boat Quay / Raffles Place / Marina": "balestiertoa_payoh",
                    "D02 Chinatown / Tanjong Pagar": "buona_vista_west_coastclementi",
                    "D03 Alexandra / Commonwealth": "east_coast_marine_parade",
                    "D04 Harbourfront / Telok Blangah": "hougang_punggol_sengkang",
                    "D05 Buono Vista / West Coast / Clementi New Town": "admiralty_woodlands",
                    "D06 City Hall / Clarke Quay": "alexandra_commonwealth",
                    "D07 Beach Road / Bugis / Rochor": "boon_lay_jurong_tuas",
                    "D08 Farrer Park / Serangoon Road": "d08_farrer_park__serangoon_road",
                    "D09 Orchard / River Valley": "d09_orchard__river_valley",
                    "D10 Tanglin / Holland / Bukit Timah": "d10_tanglin__holland__bukit_timah",
                    "D11 Newton / Novena": "d11_newton__novena",
                    "D12 Balestier / Toa Payoh": "d12_balestier__toa_payoh",
                    "D13 Macpherson / Potong Pasir": "d13_macpherson__potong_pasir",
                    "D14 Eunos / Geylang / Paya Lebar": "d14_eunos__geylang__paya_lebar",
                    "D15 East Coast / Marine Parade": "d15_east_coast__marine_parade",
                    "D16 Bedok / Upper East Coast": "d16_bedok__upper_east_coast",
                    "D17 Changi Airport / Changi Village": "d17_changi_airport__changi_village",
                    "D18 Pasir Ris / Tampines": "d18_pasir_ris__tampines",
                    "D19 Hougang / Punggol / Sengkang": "d19_hougang__punggol__sengkang",
                    "Ang Mo Kio": "d20_ang_mo_kio__bishan__thomson",
                    "D21 Clementi Park / Upper Bukit Timah": "d21_clementi_park__upper_bukit_timah",
                    "D22 Boon Lay / Jurong / Tuas": "d22_boon_lay__jurong__tuas",
                    "D23 Dairy Farm / Bukit Panjang / Choa Chu Kang": "d23_dairy_farm__bukit_panjang__choa_chu_kang",
                    "D24 Lim Chu Kang / Tengah": "d24_lim_chu_kang__tengah",
                    "D25 Admiralty / Woodlands": "d25_admiralty__woodlands",
                    "D26 Mandai / Upper Thomson": "d26_mandai__upper_thomson",
                    "D27 Sembawang / Yishun": "d27_sembawang__yishun",
                    "D28 Seletar / Yio Chu Kang": "d28_seletar__yio_chu_kang",
                    }

    # must include 1 only
    location = "search_neighborhood=" + locationList["All"] + "&"

    # must include 1 only
    roomList = {"All": "0",
                "2-Room HDB": "59",
                "3-Room HDB": "8",
                "4-Room HDB": "11",
                "5-Room HDB": "29",
                }
    # must include 1 only
    room = "search_type=" + roomList["4-Room HDB"] + "&"

    # must include 1 only
    bath = {"Any": "0",
            "1+": "1",
            "2+": "2",
            "3+": "3",
            "4+": "4",
            "5+": "5"}
    numbath = "search_baths=" + "2" + "&"

    # if no min price, "" is empty
    minPrice = "search_price_min=" + "" + "&"

    # if no max price, "" is empty
    maxPrice = "search_price_max=" + ""

    base = "https://www.bleubricks.com/page/" + str(pageNum) + "/listings/?sort=newest&search_status=61&" + location + room + numbath + minPrice + maxPrice
    return base


if __name__ == "__main__":
    main()
