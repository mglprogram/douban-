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
    name = name.strip()
    # 增强的特殊语言映射表（新增常见重复项处理）
    special_cases = {
        '汉语普通话': '普通话',
        '普通话': '普通话',  # 防止重复
        '上海话': '沪语',
        '湖南话': '湘语',
        '广东话': '粤语',
        '粤语': '粤语',  # 防止重复
        '语言': '普通话',
        '言语': '普通话',  # 处理原文中的"言语"重复
        '中国手语': '手语',
        '手语': '手语',  # 防止重复
        'Local': '本地语',  # 统一英文标识
        'PARIA': '帕里亚语',
        'POLID': '波利德语'  # 假设的映射，根据实际需求调整
    }

    # 优先检查特殊映射
    if name in special_cases:
        return special_cases[name]

    # 通用中文处理规则
    if '语' in name and len(name) > 2:
        return name[:2]  # 直接取前2字（如"西班牙"->"西班牙"，而非"西班"）
    if '话' in name and len(name) > 2:
        return name[:2] + '话'  # 保留方言标识（如"武汉话"）
    return name  # 其他情况原样返回


def getLangData():
    langList = typeList('lang')  # 假设这是获取原始语言列表的函数
    langObj = {}

    # 第一步：统一统计原始数据（未缩写）
    for lang in langList:
        lang = lang.strip()
        if lang not in langObj:
            langObj[lang] = 0
        langObj[lang] += 1

    # 第二步：处理缩写并合并统计
    merged_data = {}
    for raw_name, count in langObj.items():
        short_name = shorten_lang_name(raw_name)
        if short_name not in merged_data:
            merged_data[short_name] = 0
        merged_data[short_name] += count

    # 转换为最终输出的列表
    langRows = list(merged_data.keys())
    langColumns = list(merged_data.values())

    return langRows, langColumns
