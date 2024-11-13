from .utils import *


def getDirectorsDataTop20():
    directorsList = typeList('directors')
    directorsObj = {}
    for i in directorsList:
        if directorsObj.get(i, -1) == -1:
            directorsObj[i] = 1
        else:
            directorsObj[i] += 1
    directorsObj = sorted(directorsObj.items(), key=lambda x: x[1], reverse=True)[:20]
    row = []
    columns = []
    for i in directorsObj:
        row.append(i[0])
        columns.append(i[1])

    return row, columns


def getActorsDataTop20():
    actorsList = typeList('actors')
    actorsObj = {}
    for i in actorsList:
        if actorsObj.get(i, -1) == -1:
            actorsObj[i] = 1
        else:
            actorsObj[i] += 1
    actorsObj = sorted(actorsObj.items(), key=lambda x: x[1], reverse=True)[:20]
    actorsRow = []
    actorsColumns = []
    for i in actorsObj:
        actorsRow.append(i[0])
        actorsColumns.append(i[1])
    return actorsRow, actorsColumns
