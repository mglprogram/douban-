from .utils import *


def getMapData():
    # 获取所有国家列表
    mapList = typeList('country')
    mapObj = {}
    for i in mapList:
        if mapObj.get(i, -1) == -1:
            mapObj[i] = 1
        else:
            mapObj[i] += 1
    # 返回国家列表和对应电影数量列表
    return list(mapObj.keys()), list(mapObj.values())

# def getLangData():
#     # 获取所有语言列表
#     langList = typeList('lang')
#     langObj = {}
#     for i in langList:
#         if langObj.get(i,-1) == -1:
#             langObj[i] = 1
#         else:
#             langObj[i] += 1
#     # 返回语言列表和对应电影数量列表
#     return list(langObj.keys()), list(langObj.values())
    # 语言缩写处理函数
def shorten_lang_name(name):
    # 去除可能残留的空格
    name = name.strip()
    # 特殊语言映射表 - 优先匹配
    special_cases = {
        '汉语普通话': '普通话',
        '上海话': '沪语',
        '湖南话': '湘语',
        '广东话': '粤语',
        '语言': '普通话',
        '中国手语': '手语',
    }

    # 优先检查特殊映射
    if name in special_cases:
        return special_cases[name]

    # 通用中文处理
    if '语' in name and len(name) > 2:  # 避免单字语言被错误处理
        return name.replace('语', '')
    if '方言' in name  and len(name) > 2:
        return name.replace('方言', '话')
    return name


def getLangData():
    # 获取所有语言列表
    langList = typeList('lang')
    langObj = {}
    for i in langList:
        if langObj.get(i, -1) == -1:
            langObj[i] = 1
        else:
            langObj[i] += 1

    # 对语言名称进行缩写处理，同时保留原始名称用于tooltip
    langRows = []
    langColumns = []
    for key, value in langObj.items():
        langRows.append(shorten_lang_name(key))  # 缩写后的名称用于标签
        langColumns.append(value)

    # 返回缩写后的语言列表和对应电影数量列表
    return langRows, langColumns
