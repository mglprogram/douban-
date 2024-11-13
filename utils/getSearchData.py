import json

from .utils import *


def getMovieDetailById(movieName):
    tableData = df.values
    resultData = []
    for i in tableData:
        if i[2] == movieName:
            i[17] = i[17].split(sep=',')
            resultData.append(i)
    return resultData


def getMovieDetailBySearchWord(searchWord):
    tableData = df.values
    resultData = []
    for i in tableData:
        if i[2].find(searchWord) != -1:
            i[17] = i[17].split(sep=',')
            resultData.append(i)
    return resultData
