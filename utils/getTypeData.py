from .utils import *


def getTypeData():
    # 获取所有类型列表
    typesList = typeList('types')
    typesObj = {}
    for i in typesList:
        if typesObj.get(i, -1) == -1:
            typesObj[i] = 1
        else:
            typesObj[i] += 1
    typesData = []
    for key, item in typesObj.items():
        typesData.append({
            "name": key, # 类型名称
            "value": item # 出现次数
        })
    return typesData
