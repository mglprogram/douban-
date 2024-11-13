import pandas as pd
from sqlalchemy import create_engine

con = create_engine('mysql+pymysql://root:root@localhost:3306/dbm')

df = pd.read_sql('select * from movie', con=con)


def typeList(type):
    type = df[type].values
    type = list(map(lambda x: x.split(','), type))
    typeList = []
    for i in type:
        for j in i:
            typeList.append(j)
    return typeList


