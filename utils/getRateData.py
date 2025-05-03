import re

from .utils import *


def getAllType():
    # 获取所有不重复的电影类型
    return list(set(typeList('types')))


def getAllRateDataByType(type):
    if type == 'all':
        # 全类型时直接获取所有评分
        rateList = df['rate'].values
        rateList.sort()
    else:
        # 按类型过滤评分
        typeList = df['types'].map(lambda x: x.split(sep=','))
        oldRateList = df['rate'].values
        rateList = []
        for i, item in enumerate(typeList):
            if type in item:
                rateList.append(oldRateList[i])
    # 统计评分分布
    rateObj = {}
    for i in rateList:
        if rateObj.get(i, -1) == -1:
            rateObj[i] = 1
        else:
            rateObj[i] += 1
    # 评分值列表, 频次列表
    return list(rateObj.keys()), list(rateObj.values())


def getStars(searchIpt):
    # 获取匹配电影的星级分布数据
    stars = list(df.loc[df["title"].str.contains(searchIpt)]['stars'])[0].split(',')
    searchName = list(df.loc[df["title"].str.contains(searchIpt)]['title'])[0]
    # 初始化星级数据
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
    # 填充百分比数据（去掉%符号）
    for i, item in enumerate(stars):
        starData[i]['value'] = float(re.sub('%', '', item))
    return starData, searchName # 星级分布数据, 电影名称

def getYearMeanData():
    # 获取所有不重复年份
    yearList = list(set(df['year'].values))
    # 计算每年平均评分
    meanList = []
    for i in yearList:
        meanList.append(df[df['year'] == i]['rate'].mean())
    return yearList, meanList  # 年份列表, 平均分列表
