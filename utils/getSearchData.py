import json

from .utils import *


def getMovieDetailById(movieName):
    tableData = df.values
    resultData = []
    for i in tableData:
        # 检查电影名是否完全匹配（i[MOVIE_NAME_COLUMN]是电影名字段）
        if i[MOVIE_NAME_COLUMN] == movieName:
            # 处理图片列表字段
            i[IMG_COLUMN] = i[IMG_COLUMN].split(sep=',')
            resultData.append(i)
    return resultData


def getMovieDetailBySearchWord(searchWord):
    tableData = df.values
    resultData = []
    for i in tableData:
        # 检查电影名是否包含搜索词（模糊匹配）
        if i[MOVIE_NAME_COLUMN].find(searchWord) != -1:
            i[IMG_COLUMN] = i[IMG_COLUMN].split(sep=',')
            resultData.append(i)
    return resultData
