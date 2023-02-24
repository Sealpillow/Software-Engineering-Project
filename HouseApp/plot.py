import requests
import json
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from pathlib import Path
import os
import matplotlib
import datetime
matplotlib.use('agg')  # used for UserWarning: Starting a Matplotlib GUI outside of the main thread will likely fail.
#  https://www.dataquest.io/blog/python-api-tutorial/


def jPrint(obj):
    # create a formatted string of the Python JSON object
    # json.dumps() — Takes in a Python object, and converts (dumps) it to a string.
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def generateAnnotation(xAxis,yAxis):
    for i in range(len(xAxis)):
        plt.annotate(str(yAxis[i]),xy=(xAxis[i],yAxis[i]))


def findMinMax(dataList):
    # https://stackoverflow.com/questions/47963548/how-to-append-a-row-to-another-dataframe
    minmax = pd.DataFrame()
    minmax = minmax.append(dataList.iloc[0])
    minmax = minmax.append(dataList.iloc[0])
    for index, data in dataList.iterrows():
        price = float(data["resale_price"])
        if price < float(minmax.iloc[0]["resale_price"]):
            minmax.iloc[0] = data
        if price > float(minmax.iloc[1]["resale_price"]):
            minmax.iloc[1] = data
    minmax = minmax.reset_index(drop=True)
    return minmax


def generateGraph(filteredFrame,town,room,option,monthList,strGraph):  # option 0: generate average resale price, option 1:Overall generate average resale price
    selectedTownInfoPerMonth = []
    for i in monthList:  # xAxis
        selectedTownInfoPerMonth.append(filteredFrame[filteredFrame["month"] == i])

    totalMonth = len(selectedTownInfoPerMonth)
    numMonth = 12
    start = totalMonth - numMonth
    end = totalMonth
    minResalePricePerMonth = []
    maxResalePricePerMonth = []
    selectedTownAverageResalePricePerMonth = []
    for i in range(start, end):  # yAxis
        sum = 0
        counter = 0
        temp = []
        for j in selectedTownInfoPerMonth[i]['resale_price']:  # calculate average for that month
            counter += 1
            sum += float(j)
            temp.append(float(j))
        if counter == 0:  # if no sales of that month
            minimum = 0
            maximum = 0
            average = 0
        else:
            minimum = min(temp)      # find the lowest resale price for that month
            maximum = max(temp)      # find the highest resale price for that month
            average = sum / counter  # find the average resale price for that month
        selectedTownAverageResalePricePerMonth.append(round(average))
        minResalePricePerMonth.append(minimum)
        maxResalePricePerMonth.append(maximum)

    xMonth = monthList[start:]  # get all xAxis
    plt.figure(figsize=(30, 20))
    plt.ticklabel_format(useOffset=False, axis='y')
    plt.plot(xMonth, selectedTownAverageResalePricePerMonth)
    generateAnnotation(xMonth, selectedTownAverageResalePricePerMonth)
    if option == 1:  # option 1
        plt.xlabel('Month')
        plt.ylabel('Resale Price')
        plt.plot(xMonth, minResalePricePerMonth)
        generateAnnotation(xMonth, minResalePricePerMonth)
        plt.plot(xMonth, maxResalePricePerMonth)
        generateAnnotation(xMonth, maxResalePricePerMonth)
        #print("Overall Average Resale Price Graph Generated")
        strGraph = "static/"+strGraph
    else:
        plt.xlabel('Month')
        plt.ylabel('Average Resale Price')
        #print("Average Resale Price Graph Generated")
        strGraph = "static/"+strGraph
    plt.title(town + "(" + room + ")")
    path = Path(strGraph)
    if path.is_file():  # check file exist
        os.remove(strGraph)  # remove from directory
    plt.savefig(strGraph)
    plt.close()


def generateBar(filterMonth,option,townList,strGraph):  # min:0, avg:1, max:2
    flatInfoForEachTown = []
    for i in townList:  # xAxis
        flatInfoForEachTown.append(filterMonth[filterMonth["town"] == i])

    averageResalePricePerTown = []
    for i in range(len(flatInfoForEachTown)):  # yAxis
        if option == 0:
            if len(flatInfoForEachTown[i]['resale_price']):
                averageResalePricePerTown.append(float(min(flatInfoForEachTown[i]['resale_price'])))
            else:
                averageResalePricePerTown.append(0)
        if option == 1:
            counter = 0
            sum = 0
            for j in flatInfoForEachTown[i]['resale_price']:
                counter += 1
                sum += float(j)
            if counter == 0:
                average = 0
            else:
                average = sum / counter
            averageResalePricePerTown.append(round(average))
        if option == 2:
            if len(flatInfoForEachTown[i]['resale_price']):
                averageResalePricePerTown.append(float(max(flatInfoForEachTown[i]['resale_price'])))
            else:
                averageResalePricePerTown.append(0)

    plt.figure(figsize=(50, 30))
    plt.xlabel('Town Name')
    plt.ylabel('Average Resale Price')
    plt.bar(townList, averageResalePricePerTown)
    generateAnnotation(townList,averageResalePricePerTown)

    strGraph = "static/"+strGraph
    path = Path(strGraph)
    if path.is_file():  # check file exist
        os.remove(strGraph)  # remove from directory
    plt.savefig(strGraph)
    plt.close()


def generateCount(filterMonth,strGraph):

    plt.figure(figsize=(50, 30))
    countOrder = filterMonth.town.value_counts().index.tolist()
    ax = sb.countplot(y="town", data=filterMonth, order= countOrder, orient='h')
    for p in ax.patches:
        ax.annotate(int(p.get_width()), ((p.get_x() + p.get_width()+1.2), p.get_y()), xytext=(1, -18), fontsize=9, color='#004d00', textcoords='offset points', horizontalalignment='right')
    strGraph = "static/" + strGraph
    path = Path(strGraph)
    if path.is_file():  # check file exist
        os.remove(strGraph)  # remove from directory
    plt.savefig(strGraph)
    plt.close()

# If you want to read a json file -> json.loads() — Takes a JSON string, and converts (loads) it to a Python object.
# https://chartio.com/resources/tutorials/how-to-save-a-plot-to-a-file-using-matplotlib/

# API
# https://data.gov.sg/dataset/resale-flat-prices


def main(inputLocationsList,inputRoomsList):

    directory = '..\HouseApp\static'
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            os.remove(os.path.join(directory, filename))

    response = requests.get("https://data.gov.sg/api/action/datastore_search?resource_id=f1765b54-a209-4718-8d38-a39237f502b3&limit=145156")
    if response.status_code !=200:
        print("Api cant be found")
    data = response.json()
    Data = pd.DataFrame(data["result"]["records"])
    month = Data["month"]
    monthList = month.unique().tolist()

    town = Data["town"]
    townList = town.unique().tolist()
    flatInfoPerTown = {}
    # append every data based on the town
    for i in townList:
        flatInfoPerTown[i] = Data[Data["town"] == i]

    # General data, month (m) set based on prev month
    m = "2023-01"
    # get previous month data
    now = datetime.datetime.now()
    current_year = str(now.year)
    prev_month = now.month - 1 if now.month - 1 > 0 else 12  # if month is jan:1 prev month will be dec:12
    strMonth = ('0'+str(prev_month)) if prev_month<10 else str(prev_month)
    date = current_year+"-"+strMonth
    filterMonth = Data[Data["month"] == date]
    generateBar(filterMonth, 0, townList,"0.png")  # find the min resale price based on filter on that month
    generateBar(filterMonth, 1, townList,"1.png")  # find the avg resale price based on filter on that month
    generateBar(filterMonth, 2, townList,"2.png")  # find the max resale price based on filter on that month
    generateCount(filterMonth,"3.png")  # find the num of resale flats based on filter on that month

    count = 4
    for inputTown in inputLocationsList: # user input
        filterTown = flatInfoPerTown[inputTown.upper()]
        for inputRoom in inputRoomsList:  # user input
            filterRoom = filterTown[filterTown["flat_type"] == inputRoom.upper()]
            # Specific data filter: town: BEDOK, room = 5 ROOM   -> if room not stated, assumed to be all
            # generateGraph(filterRoom, inputTown, inputRoom, 0, monthList,str(count)+".png")  # find the Average Resale Price based on filter and the past 12 months
            generateGraph(filterRoom, inputTown, inputRoom, 1, monthList,str(count)+".png")  # find the Overall Resale Price based on filter and the past 12 months
            count += 1
            # print(findMinMax(filterRoom)) #

if __name__ == "__main__":
    main()


