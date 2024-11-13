from .query import *


def delMovieByMovieName(movieName):
    sql = 'delete from movie where title = %s'
    querys(sql, [movieName])
    return '删除成功'


def getTableDataByTablePage():
    sql = 'select * from movie'
    data = list(querys(sql, [], 'select'))

    def map_fn(item):
        item = list(item)
        item[17] = item[17].split(sep=',')
        return item

    data = list(map(map_fn, data))
    return data
