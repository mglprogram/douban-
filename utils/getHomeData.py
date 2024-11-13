from .utils import *


def getHomeData():
    maxMovieLen = len(df.values)
    maxRate = df['rate'].max()
    actorsList = typeList('actors')
    maxActors = max(actorsList, key=actorsList.count)
    countryList = typeList('country')
    maxCountry = max(countryList, key=countryList.count)
    typesList = typeList('types')
    maxTypes = len(set(typesList))
    langList = typeList('lang')
    maxLang = max(langList, key=langList.count)

    return maxMovieLen, maxRate, maxActors, maxCountry, maxTypes, maxLang


def getTypesEchartsData():
    typesList = typeList('types')
    typeObj = {}
    for i in typesList:
        if typeObj.get(i, -1) == -1:
            typeObj[i] = 1
        else:
            typeObj[i] += 1
    typeEchartsData = []
    for key, value in typeObj.items():
        typeEchartsData.append({
            'key': key,
            'value': value
        })
    return typeEchartsData


def getRateEchartsData():
    rateList = df['rate'].map(lambda x: float(x)).values
    rateList.sort()
    rateObj = {}
    for i in rateList:
        if rateObj.get(i, -1) == -1:
            rateObj[i] = 1
        else:
            rateObj[i] += 1
    return list(rateObj.keys()), list(rateObj.values())


def getTableData():
    tableData = df.values
    for i, item in enumerate(tableData):
        item[17] = item[17].split(sep=',')
    return tableData


# def getMovieUrlByName(movieName):
#     tableData = df[df['title'] == movieName].values[0]
#     return tableData[-1]
