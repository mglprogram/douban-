from pymysql import *

conn = connect(host='localhost', user='root', password='root', database='dbm', port=3306)
cursor = conn.cursor()


def querys(sql, params, type='no_select'):
    params = tuple(params)
    cursor.execute(sql, params)
    if type != 'no_select':  # 查询语句
        data_list = cursor.fetchall()
        conn.commit()
        return data_list
    else:  # 操作数据库
        conn.commit()
        return "数据库语句执行成功"
