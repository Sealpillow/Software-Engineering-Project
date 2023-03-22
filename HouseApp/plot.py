import requests
import json
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from pathlib import Path
import os
import matplotlib
import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from datetime import datetime
import time


matplotlib.use('agg')  # used for UserWarning: Starting a Matplotlib GUI outside of the main thread will likely fail.
#  https://www.dataquest.io/blog/python-api-tutorial/


def generateAnnotation(xAxis, yAxis):
    """
    This function annotate str values to its plot

    Args:
        xAxis (list): List of string containing x-axis values
        yAxis (list): List of string/int containing y-axis values
    """
    for i in range(len(xAxis)):
        plt.annotate(str(yAxis[i]), xy=(xAxis[i], yAxis[i]), fontsize=15)


def generateGraph(filteredFrame, town, room, monthList, strGraph):  # option 0: generate average resale price, option 1:Overall generate average resale price
    """
    This function generate Min/Average/Max ResalePricePerMonth graph based on filtered data frame

    Args:
        filteredFrame (pandas.core.frame.DataFrame): filtered dataframe based on location and flatType
        town (str): Str of town
        room (str): Str of room
        monthList (list): list of the month
        strGraph (str): png name
    """
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
    for i in range(start, end - 1):  # yAxis, -1 to excluded current month
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
            minimum = min(temp)  # find the lowest resale price for that month
            maximum = max(temp)  # find the highest resale price for that month
            average = sum / counter  # find the average resale price for that month
        selectedTownAverageResalePricePerMonth.append(round(average))
        minResalePricePerMonth.append(minimum)
        maxResalePricePerMonth.append(maximum)

    xMonth = monthList[start:-1]  # get all xAxis, -1 to excluded current month
    plt.figure(figsize=(30, 20))
    plt.ticklabel_format(useOffset=False, axis='y')
    plt.plot(xMonth, selectedTownAverageResalePricePerMonth)
    generateAnnotation(xMonth, selectedTownAverageResalePricePerMonth)
    plt.xlabel('Month')
    plt.ylabel('Resale Price')
    plt.plot(xMonth, minResalePricePerMonth)
    generateAnnotation(xMonth, minResalePricePerMonth)
    plt.plot(xMonth, maxResalePricePerMonth)
    generateAnnotation(xMonth, maxResalePricePerMonth)
    # print("Overall Average Resale Price Graph Generated")
    plt.title(town + "(" + room + ")")
    path = Path(strGraph)
    if path.is_file():  # check file exist
        os.remove(strGraph)  # remove from directory
    plt.savefig(strGraph)
    plt.close()


def generateBar(filterMonth, option, townList, strGraph):  # min:0, avg:1, max:2
    """
    This function generate Min/Average/Max ResalePricePerMonth graph based on filtered data frame

    Args:
        filterMonth (pandas.core.frame.DataFrame): filtered dataframe based on month
        option (int): option that determine what kind of bar graph, 0:min 1:avg 2:max
        townList (list): list of towns in singapore
        strGraph (str): png name
    """
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
        elif option == 1:
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
        elif option == 2:
            if len(flatInfoForEachTown[i]['resale_price']):
                averageResalePricePerTown.append(float(max(flatInfoForEachTown[i]['resale_price'])))
            else:
                averageResalePricePerTown.append(0)

    plt.figure(figsize=(50, 30))
    plt.xlabel('Town Name')
    plt.ylabel('Average Resale Price')
    plt.bar(townList, averageResalePricePerTown)
    generateAnnotation(townList, averageResalePricePerTown)

    path = Path(strGraph)
    if path.is_file():  # check file exist
        os.remove(strGraph)  # remove from directory
    plt.savefig(strGraph)
    plt.close()


def generateCount(filterMonth, townList, strGraph):
    """
    This function generate the count plot based on num of resale flats and filter on that month

    Args:
        filterMonth (pandas.core.frame.DataFrame): filtered dataframe based on month
        townList (list): list of towns in singapore
        strGraph (str): png name
    """
    plt.figure(figsize=(50, 30))
    countOrder = filterMonth.town.value_counts().index.tolist()
    if len(countOrder) == 0:  # in a case where there is no sale for that month for all of the locations
        # create empty dataframe with desired columns
        df = pd.DataFrame(columns=townList)

        # create count plot with no data but with columns
        sb.countplot(data=df, orient='h')

        # set axis labels and ticks
        plt.ylabel('Town')
        plt.xlabel('Count')
        plt.xlim(0, 100)
    else:
        ax = sb.countplot(y="town", data=filterMonth, order=countOrder, orient='h')
        for p in ax.patches:
            ax.annotate(int(p.get_width()), ((p.get_x() + p.get_width() + 1.2), p.get_y()), xytext=(1, -18), fontsize=15, color='#004d00', textcoords='offset points', horizontalalignment='right')
    path = Path(strGraph)
    if path.is_file():  # check file exist
        os.remove(strGraph)  # remove from directory
    plt.savefig(strGraph)
    plt.close()


def to_seconds(date):
    return time.mktime(date.timetuple())


def linearRegression(predictor, response, testsize, strGraph): 
    # train_test_split returns 4 values
    # Split the Dataset into Train and Test, with test_size= 0.2 if predictor total 1000, X_train: 800 data pts, X_test: 200 data pts 
    X_train, X_test, y_train, y_test = train_test_split(predictor, response, test_size = testsize)


    # Linear Regression using Train Data
    linreg = LinearRegression()         # create the linear regression object
    linreg.fit(X_train, y_train)        # train the linear regression model

    # Coefficients of the Linear Regression line
    print('Intercept of Regression \t: b = ', linreg.intercept_)
    print('Coefficients of Regression \t: a = ', linreg.coef_)
    print()

    # Predict Total values corresponding to HP
    y_train_pred = linreg.predict(X_train)
    y_test_pred = linreg.predict(X_test)
    print(y_test_pred)
    # Check the Goodness of Fit (on Train Data)
    print("Goodness of Fit of Model \tTrain Dataset")
    print("Explained Variance (R^2) \t:", linreg.score(X_train, y_train))
    print("Mean Squared Error (MSE) \t:", mean_squared_error(y_train, y_train_pred))
    print()

    # Check the Goodness of Fit (on Test Data)
    print("Goodness of Fit of Model \tTest Dataset")
    print("Explained Variance (R^2) \t:", linreg.score(X_test, y_test))
    print("Mean Squared Error (MSE) \t:", mean_squared_error(y_test, y_test_pred))
    print()

    # Plot the Predictions vs the True values
    f, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].scatter(y_train, y_train_pred, color = "blue")
    axes[0].plot(y_train, y_train, 'r-', linewidth = 1)
    axes[0].set_xlabel("True values of the Response Variable (Train)")
    axes[0].set_ylabel("Predicted values of the Response Variable (Train)")
    axes[1].scatter(y_test, y_test_pred, color = "green")
    axes[1].plot(y_test, y_test, 'r-', linewidth = 1)
    axes[1].set_xlabel("True values of the Response Variable (Test)")
    axes[1].set_ylabel("Predicted values of the Response Variable (Test)")

    
    path = Path(strGraph)
    if path.is_file():  # check file exist
        os.remove(strGraph)  # remove from directory
    plt.savefig(strGraph)
    plt.close()

def generateLinearRegression(filteredFrame, option, strGraph):
    """
    This function generates the regression line based on the filtered data frame

    Args:
        filteredFrame (pandas.core.frame.DataFrame): filtered dataframe based on location and flatType
        option (int): option that determines which predictor to use, 0:floor area 1: time of resale 2: remaining lease
        strGraph (str): png name
    """
    price = pd.DataFrame(filteredFrame['resale_price'].astype(float))
    if len(price) == 0: return
    if option == 0:
        area = pd.DataFrame(filteredFrame['floor_area_sqm'].astype(float))
        linearRegression(area, price, 0.2, strGraph)
    elif option == 1:
        months = filteredFrame["month"]

        months_timestamp = []
        for month in months: 
            date = datetime.strptime(month, '%Y-%m').date()
            timestamp = to_seconds(date)
            months_timestamp.append(timestamp)

        months_timestamp_df = pd.DataFrame(months_timestamp)
        months_timestamp_df.rename({0:"timestamp"}, axis=1, inplace=True)

        linearRegression(months_timestamp_df,price,0.2, strGraph)
    elif option == 2:
        remainingLease = filteredFrame["remaining_lease"]
        remainingLeaseFloat = []
        for lease in remainingLease:
            leaseYear = float(lease[0:2])  
            if lease[9:11] == '':
                leaseMonth = 0
            else: 
                leaseMonth = float(lease[9:11])

            if (leaseMonth == 0):
                leaseFloat = leaseYear
            else:
                leaseFloat = leaseYear + leaseMonth/12
            remainingLeaseFloat.append(round(leaseFloat, 2))
        remainingLeaseFloat = pd.DataFrame(remainingLeaseFloat)
        remainingLeaseFloat.rename({0:"remaining lease (years)"}, axis=1, inplace=True)
        linearRegression(remainingLeaseFloat, price, 0.2, strGraph)

def generateHeatMap(filteredMonth, strGraph):
    sb.set(rc={'figure.figsize':(11.7,8.27)})
    price = pd.DataFrame(filteredMonth['resale_price'].astype(float))
    if len(price) == 0: 
        return
    else:
        area = pd.DataFrame(filteredMonth['floor_area_sqm'].astype(float))
        remainingLease = pd.DataFrame(filteredMonth['remaining_lease'])
        remainingLease = filteredMonth["remaining_lease"]
        remainingLeaseFloat = []
        for lease in remainingLease:
            leaseYear = float(lease[0:2])  
            if lease[9:11] == '':
                leaseMonth = 0
            else: 
                leaseMonth = float(lease[9:11])

            if (leaseMonth == 0):
                leaseFloat = leaseYear
            else:
                leaseFloat = leaseYear + leaseMonth/12
            remainingLeaseFloat.append(float(round(leaseFloat, 2)))
        remainingLeaseFloat = pd.DataFrame(remainingLeaseFloat)
        remainingLeaseFloat.rename({0:"remaining lease (years)"}, axis=1, inplace=True)
        remainingLeaseFloat = pd.DataFrame(remainingLeaseFloat["remaining lease (years)"].astype(float))
        joinedDF = price
        joinedDF = joinedDF.join(area)
        joinedDF = joinedDF.join(remainingLeaseFloat)
        print(joinedDF.info())
        sb.heatmap(joinedDF.corr(), annot=True, fmt=".2f")

    path = Path(strGraph)
    if path.is_file():  # check file exist
        os.remove(strGraph)  # remove from directory
    plt.savefig(strGraph)
    plt.close()

        


# If you want to read a json file -> json.loads() — Takes a JSON string, and converts (loads) it to a Python object.
# https://chartio.com/resources/tutorials/how-to-save-a-plot-to-a-file-using-matplotlib/

# API
# https://data.gov.sg/dataset/resale-flat-prices

def main(inputLocationsList, inputRoomsList):
    """
    This is the main function of the script that generate analysis PNG based on inputs

    It calls function1() and function2() to do something useful.
    Args:
        inputLocationsList (list): contain list of location option
        inputRoomsList (list): contain list of room option
    """
    path = "./HouseApp/static/" # if visual studio
    # path = "static/"  # if pycharm
    for filename in os.listdir(path):
        if filename.endswith('.png'):
            os.remove(os.path.join(path, filename))
    response = requests.get("https://data.gov.sg/api/action/datastore_search?resource_id=f1765b54-a209-4718-8d38-a39237f502b3")
    data = response.json()
    recordLimit = data['result']['total']
    response = requests.get("https://data.gov.sg/api/action/datastore_search?resource_id=f1765b54-a209-4718-8d38-a39237f502b3&limit=" + str(recordLimit))
    if response.status_code != 200:
        print("Api cant be found")
    data = response.json()
    Data = pd.DataFrame(data["result"]["records"])
    month = Data["month"]
    monthList = month.unique().tolist()

    town = Data["town"]
    townList = town.unique().tolist()

    # get previous month data
    now = datetime.now()
    current_year = str(now.year)
    prev_month = now.month - 1 if now.month - 1 > 0 else 12  # if month is jan:1 prev month will be dec:12
    strMonth = ('0' + str(prev_month)) if prev_month < 10 else str(prev_month)
    date = current_year + "-" + strMonth
    filterMonth = Data[Data["month"] == date]

    flatInfoPerTown = {}
    # append every data based on the town
    for i in townList:
        flatInfoPerTown[i] = Data[Data["town"] == i]

    generateBar(filterMonth, 0, townList, path + "0.png")  # find the min resale price based on filter on that month
    generateBar(filterMonth, 1, townList, path + "1.png")  # find the avg resale price based on filter on that month
    generateBar(filterMonth, 2, townList, path + "2.png")  # find the max resale price based on filter on that month
    generateCount(filterMonth, townList, path + "3.png")  # find the num of resale flats based on filter on that month
    generateHeatMap(filterMonth, path + "4.png")
    count = 5 # change to 5 after above done
    for inputTown in inputLocationsList:  # user input
        filterTown = flatInfoPerTown[inputTown.upper()]
        for inputRoom in inputRoomsList:  # user input
            filterRoom = filterTown[filterTown["flat_type"] == inputRoom.upper()]
            # Specific data filter: town: BEDOK, room = 5 ROOM   -> if room not stated, assumed to be all
            generateGraph(filterRoom, inputTown, inputRoom, monthList, path + str(count) + ".png")  # find the Overall Resale Price based on filter and the past 12 months
            count += 1

if __name__ == "__main__":
    main()
