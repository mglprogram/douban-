from pymysql import *

conn = connect(host='localhost', user='root', password='root', database='dbm', port=3306)
cursor = conn.cursor()

# 定义通用数据库查询函数
def querys(sql, params, type='no_select'):
    # 将参数转换为元组（确保SQL参数安全）
    params = tuple(params)
    # 执行SQL语句（参数化查询，防止SQL注入）
    cursor.execute(sql, params)
    if type != 'no_select':  # 判断是否为查询语句（SELECT）
        # 获取查询结果（所有行）
        data_list = cursor.fetchall()
        conn.commit()
        return data_list
    else:  # 操作数据库
        # 非查询语句（INSERT/UPDATE/DELETE等）直接提交事务
        conn.commit()
        return "数据库语句执行成功"
