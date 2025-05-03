import pandas as pd
from sqlalchemy import create_engine

# 电影名字段
MOVIE_NAME_COLUMN = 2
# 图片列
IMG_COLUMN = 17
# 创建MySQL数据库连接引擎
# 格式：mysql+pymysql://用户名:密码@主机:端口/数据库名
con = create_engine('mysql+pymysql://root:root@localhost:3306/dbm')

df = pd.read_sql('select * from movie', con=con)

# 定义处理多值字段的函数
def typeList(type):
    # 获取指定列的所有值（numpy数组）
    type = df[type].values
    # 将每个值按逗号分割，生成二维列表
    type = list(map(lambda x: x.split(','), type))
    typeList = []
    for i in type:
        for j in i:
            typeList.append(j)
    return typeList


