from .utils import *
import datetime


def getYearData():
    timeList = list(df['time'].map(lambda x: int(x[:4])))
    timeList.sort()
    timeObj = {}
    for i in timeList:
        if timeObj.get(i, -1) == -1:
            timeObj[i] = 1
        else:
            timeObj[i] = timeObj[i] + 1
    return list(timeObj.keys()), list(timeObj.values())


def getMovieTimeData():
    movieTime = list(df['movieTime'])
    movieTimeData = [{
        'name': '0-60',
        'value': 0
    }, {
        'name': '60-120',
        'value': 0
    }, {
        'name': '120-150',
        'value': 0
    }, {
        'name': '150以上',
        'value': 0
    }]
    for i in movieTime:
        if int(i) <= 60:
            movieTimeData[0]['value'] = movieTimeData[0]['value'] + 1
        elif int(i) <= 120:
            movieTimeData[1]['value'] = movieTimeData[1]['value'] + 1
        elif int(i) <= 150:
            movieTimeData[2]['value'] = movieTimeData[2]['value'] + 1
        else:
            movieTimeData[3]['value'] = movieTimeData[3]['value'] + 1
    return movieTimeData
