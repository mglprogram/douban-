from .utils import *


def getDirectorsDataTop20():
    directorsList = typeList('directors')
    directorsObj = {}
    for i in directorsList:
        if directorsObj.get(i, -1) == -1:
            directorsObj[i] = 1
        else:
            directorsObj[i] += 1
    # 按出现次数降序排序并取前20
    directorsObj = sorted(directorsObj.items(), key=lambda x: x[1], reverse=True)[:20]
    # 分离名称和计数
    row = []
    columns = []
    for i in directorsObj:
        row.append(i[0])     # 导演名称
        columns.append(i[1])     # 出现次数

    return row, columns


def getActorsDataTop20():
    # 获取所有演员列表
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
        actorsRow.append(i[0])     # 演员名称
        actorsColumns.append(i[1])     # 出现次数
    return actorsRow, actorsColumns
