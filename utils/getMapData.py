from .utils import *

def getMapData():
    mapList = typeList('country')
    mapObj = {}
    for i in mapList:
        if mapObj.get(i,-1) == -1:
            mapObj[i] = 1
        else:
            mapObj[i] += 1
    return list(mapObj.keys()), list(mapObj.values())


def getLangData():
    langList = typeList('lang')
    langObj = {}
    for i in langList:
        if langObj.get(i,-1) == -1:
            langObj[i] = 1
        else:
            langObj[i] += 1
    return list(langObj.keys()), list(langObj.values())