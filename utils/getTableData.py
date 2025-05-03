from .query import *
from .utils import IMG_COLUMN


def delMovieByMovieName(movieName):
    sql = 'delete from movie where title = %s'
    # 执行SQL查询（使用参数化查询防止SQL注入）
    querys(sql, [movieName])
    return '删除成功'


def getTableDataByTablePage():
    sql = 'select * from movie'
    # 执行查询并将结果转换为列表
    data = list(querys(sql, [], 'select'))
    # 用于处理每行数据
    def map_fn(item):
        # 将元组转换为列表（使其可变）
        item = list(item)
        item[IMG_COLUMN] = item[IMG_COLUMN].split(sep=',')
        return item

    # 将元组转换为列表（使其可变）
    data = list(map(map_fn, data))
    return data
