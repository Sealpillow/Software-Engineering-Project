import requests
import json
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import os
import matplotlib
import datetime
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px

matplotlib.use('agg')  # used for UserWarning: Starting a Matplotlib GUI outside the main thread will likely fail.
#  https://www.dataquest.io/blog/python-api-tutorial/


def generateAnnotation(xAxis, yAxis):
    """
    This function annotate str values to its plot

    Args:
        xAxis (list): List of string containing x-axis values
        yAxis (list): List of string/int containing y-axis values
    """
    for i in range(len(xAxis)):
        plt.annotate(str(yAxis[i]), xy=(xAxis[i], yAxis[i]))


def generateGraph(filteredFrame, town, room, monthList):  # option 0: generate average resale price, option 1:Overall generate average resale price
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

    # Create a figure with multiple lines
    fig = go.Figure()

    # Add the first line to the figure
    fig.add_trace(go.Scatter(x=xMonth, y=selectedTownAverageResalePricePerMonth, mode='lines+text', name='Line 1', text=selectedTownAverageResalePricePerMonth))

    # Add the second line to the figure
    fig.add_trace(go.Scatter(x=xMonth, y=minResalePricePerMonth, mode='lines+text', name='Line 1', text=minResalePricePerMonth))

    # Add the third line to the figure
    fig.add_trace(go.Scatter(x=xMonth, y=maxResalePricePerMonth, mode='lines+text', name='Line 1', text=maxResalePricePerMonth))

    # plt.title(town + "(" + room + ")")

    # convert the plot to HTML
    html_fig = fig.to_html(full_html=False)

    # modify the CSS style to make it look like an image
    # html_fig = html_fig.replace("<div class=\"mpld3-figure\">", "<div class=\"mpld3-figure\" style=\"display:inline-block; border:1px solid black; padding:5px; width:400px; height:300px; margin: 0 auto;\">")
    return html_fig


def generateBar(filterMonth, option, townList):  # min:0, avg:1, max:2
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

    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Bar(x=townList, y=averageResalePricePerTown, name="bar", text=averageResalePricePerTown,textangle=0))

    html_fig = fig.to_html(full_html=False)

    # modify the CSS style to make it look like an image
    # html_fig = html_fig.replace("<div class=\"mpld3-figure\">", "<div class=\"mpld3-figure\" style=\"display:inline-block; border:1px solid black; padding:5px; width:400px; height:300px; margin: 0 auto;\">")
    return html_fig


def generateCount(filterMonth, townList):
    """
    This function generate the count plot based on num of resale flats and filter on that month

    Args:
        filterMonth (pandas.core.frame.DataFrame): filtered dataframe based on month
        townList (list): list of towns in singapore
        strGraph (str): png name
    """
    # Calculate the count for each category and sort in descending order
    counts = filterMonth.town.value_counts().sort_values(ascending=False)

    # Create lists of categories and their counts
    categories = counts.index.tolist()
    category_counts = counts.tolist()

    # Use Plotly to create a count plot
    fig = px.histogram(x=categories, y=category_counts, text_auto=True)
    fig.update_layout(
        xaxis_title="Town", yaxis_title="Count"
    )
    # convert the plot to HTML
    html_fig = fig.to_html(full_html=False)
    # modify the CSS style to make it look like an image
    # html_fig = html_fig.replace("<div class=\"mpld3-figure\">", "<div class=\"mpld3-figure\" style=\"display:inline-block; border:1px solid black; padding:5px; width:400px; height:300px; margin: 0 auto;\">")
    return html_fig


def generateHeatMap(filterMonth,townList,option):
    df = filterMonth.drop(columns=['_id', 'block', 'street_name', 'storey_range', 'month', 'lease_commence_date'])
    price = pd.DataFrame(df['resale_price'].astype(float))
    joinedDF = price
    if option == 0:
        area = pd.DataFrame(df['floor_area_sqm'].astype(float))
        joinedDF = joinedDF.join(area)
    elif option == 1:
        df_dummies = pd.get_dummies(df['town'])
        df_new = pd.concat([df, df_dummies], axis=1)
        del df_new['town']
        town = pd.DataFrame(df_new[townList])
        joinedDF = joinedDF.join(town)
    corr_matrix = joinedDF.corr().sort_values(by='resale_price',ascending=False)
    corr_series = corr_matrix['resale_price'].iloc[1:]
    print(corr_series.sort_values(ascending=False))
    fig = px.imshow(corr_matrix, text_auto=True,height=1000, aspect="auto")

    # convert the plot to HTML
    html_fig = fig.to_html(full_html=False)
    # modify the CSS style to make it look like an image
    # html_fig = html_fig.replace("<div class=\"mpld3-figure\">", "<div class=\"mpld3-figure\" style=\"display:inline-block; border:1px solid black; padding:5px; width:400px; height:300px; margin: 0 auto;\">")
    return html_fig


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
    # path = "./HouseApp/static/" # if visual studio
    path = "static/"  # if pycharm
    for filename in os.listdir(path):
        if filename.endswith('.png'):
            os.remove(os.path.join(path, filename))
    response = requests.get("https://data.gov.sg/api/action/datastore_search?resource_id=f1765b54-a209-4718-8d38-a39237f502b3")
    data = response.json()
    recordLimit = data['result']['total']
    print(recordLimit)
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
    now = datetime.datetime.now()
    current_year = str(now.year)
    prev_month = now.month - 1 if now.month - 1 > 0 else 12  # if month is jan:1 prev month will be dec:12
    strMonth = ('0' + str(prev_month)) if prev_month < 10 else str(prev_month)
    date = current_year + "-" + strMonth
    filterMonth = Data[Data["month"] == date]

    flatInfoPerTown = {}
    # append every data based on the town
    for i in townList:
        flatInfoPerTown[i] = Data[Data["town"] == i]

    plotImages = []
    plotImages.append(generateBar(filterMonth, 0, townList))  # find the min resale price based on filter on that month
    plotImages.append(generateBar(filterMonth, 1, townList))  # find the avg resale price based on filter on that month
    plotImages.append(generateBar(filterMonth, 2, townList))  # find the max resale price based on filter on that month
    plotImages.append(generateCount(filterMonth, townList))  # find the num of resale flats based on filter on that month
    plotImages.append(generateHeatMap(filterMonth,townList,0))
    plotImages.append(generateHeatMap(filterMonth, townList, 1))

    for inputTown in inputLocationsList:  # user input
        filterTown = flatInfoPerTown[inputTown.upper()]
        for inputRoom in inputRoomsList:  # user input
            filterRoom = filterTown[filterTown["flat_type"] == inputRoom.upper()]
            # Specific data filter: town: BEDOK, room = 5 ROOM   -> if room not stated, assumed to be all
            plotImages.append(generateGraph(filterRoom, inputTown, inputRoom, monthList))  # find the Overall Resale Price based on filter and the past 12 months
    return plotImages


if __name__ == "__main__":
    main()
