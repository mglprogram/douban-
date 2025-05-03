from .utils import *


def getHomeData():
    # 电影总数
    maxMovieLen = len(df.values)
    # 电影评分
    df['rate'] = df['rate'].map(lambda x: float(x))
    maxRate = df['rate'].max()
    # 出现最多的演员
    actorsList = typeList('actors')
    maxActors = max(actorsList, key=actorsList.count)
    # 出现最多的国家
    countryList = typeList('country')
    maxCountry = max(countryList, key=countryList.count)
    # 出现最多的类型
    typesList = typeList('types')
    maxTypes = len(set(typesList))
    # 出现最多的语言
    langList = typeList('lang')
    maxLang = max(langList, key=langList.count)

    return maxMovieLen, maxRate, maxActors, maxCountry, maxTypes, maxLang


def getTypesEchartsData():
    # 获取所有电影类型列表（调用typeList函数处理逗号分隔的字符串）
    typesList = typeList('types')

    typeObj = {}
    # 遍历所有电影类型
    for i in typesList:
        # 检查类型是否已在字典中（get方法默认返回-1）
        if typeObj.get(i, -1) == -1:
            typeObj[i] = 1
        else:
            typeObj[i] += 1
    # 格式化数据为ECharts需要的结构
    typeEchartsData = []
    for key, value in typeObj.items():
        typeEchartsData.append({
            # 饼图数据必须包含name和value字段
            'name': key,
            'value': value
        })
    return typeEchartsData


def getRateEchartsData():
    # 提取评分列，转换为float类型（原数据可能是字符串） 转换为NumPy数组
    rateList = df['rate'].map(lambda x: float(x)).values
    rateList.sort()
    rateObj = {}  # 用于存储评分和出现次数的映射
    # 遍历所有评分
    for i in rateList:
        if rateObj.get(i, -1) == -1:
            rateObj[i] = 1
        else:
            rateObj[i] += 1
    # 返回两个列表：评分值列表、对应出现次数列表
    return list(rateObj.keys()), list(rateObj.values())


def getTableData():
    # 获取DataFrame的原始值（numpy二维数组）
    tableData = df.values
    # 遍历每一行数据
    for i, item in enumerate(tableData):
        # 假设第17列是逗号分隔的字符串，拆分为列表
        item[IMG_COLUMN] = item[IMG_COLUMN].split(sep=',')
    return tableData


