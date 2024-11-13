import re

from .utils import *


def getAllType():
    return list(set(typeList('types')))


def getAllRateDataByType(type):
    if type == 'all':
        rateList = df['rate'].values
        rateList.sort()
    else:
        typeList = df['types'].map(lambda x: x.split(sep=','))
        oldRateList = df['rate'].values
        rateList = []
        for i, item in enumerate(typeList):
            if type in item:
                rateList.append(oldRateList[i])
    rateObj = {}
    for i in rateList:
        if rateObj.get(i, -1) == -1:
            rateObj[i] = 1
        else:
            rateObj[i] += 1

    return list(rateObj.keys()), list(rateObj.values())


def getStars(searchIpt):
    stars = list(df.loc[df["title"].str.contains(searchIpt)]['stars'])[0].split(',')
    searchName = list(df.loc[df["title"].str.contains(searchIpt)]['title'])[0]
    starData = [{
        'name': '五星',
        'value': 0
    }, {
        'name': '四星',
        'value': 0
    }, {
        'name': '三星',
        'value': 0
    }, {
        'name': '二星',
        'value': 0
    }, {
        'name': '一星',
        'value': 0
    }]
    for i, item in enumerate(stars):
        starData[i]['value'] = float(re.sub('%', '', item))
    return starData, searchName

def getYearMeanData():
    yearList = list(set(df['year'].values))
    meanList = []
    for i in yearList:
        meanList.append(df[df['year'] == i]['rate'].mean())
    return yearList, meanList
