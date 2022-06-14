import csv

import dateutil.parser as dateParser
import requests

activities = []


def getActivitiesBody():
    return {
        "activities": activities
    }


def postActivities():
    url = 'https://ghostfol.io/api/v1/import'
    headers = {
        'Authorization': 'Bearer xxx'}
    x = requests.post(url, json=getActivitiesBody(), headers=headers)
    print(x.text)
    print(getActivitiesBody())
    global activities
    activities = []


def addActivity(activity):
    activities.append(activity)
    if (len(activities) > 19):
        postActivities()


def mutateSymbol(symbol):
    if (symbol == 'BMW3'):
        return 'BMW3.DE'
    return symbol


def createBody(row):
    return {
        "dataSource": "YAHOO",
        "date": dateParser.parse(row[1]).isoformat(),
        "currency": row[7],
        "fee": 0,
        "quantity": float(row[5]),
        "symbol": mutateSymbol(row[3]),
        "unitPrice": float(row[6])
    }


def createBuyBody(row):
    body = createBody(row)
    body['type'] = 'BUY'
    return body


def createDividendBody(row):
    body = createBody(row)
    body['type'] = 'DIVIDEND'
    return body


def createSellBody(row):
    body = createBody(row)
    body['type'] = 'SELL'
    return body


def handleRow(row):
    if (row[0] == 'Market buy'):
        activity = createBuyBody(row)
        addActivity(activity)
        # print(json.dumps(activity))
    elif (row[0] == 'Market sell'):
        activity = createSellBody(row)
        addActivity(activity)
        # print(json.dumps(activity))
    elif ('Dividend' in row[0]):
        activity = createDividendBody(row)
        addActivity(activity)
        # print(json.dumps(activity))


with open('sheets/from_2020-03-01_to_2020-12-31_MTY1NDExNDQ1NzIyMA.csv') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        handleRow(row)
