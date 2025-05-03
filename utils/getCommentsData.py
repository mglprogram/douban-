from .utils import *
import json
import sys
sys.path.append('..')
from word_cloud import *

def getCommentsImage(searchIpt):
    # 在DataFrame中查找标题包含searchIpt的电影，返回第一个匹配的完整标题
    # 使用str.contains()进行模糊匹配，[0]取第一个结果
    searchName = list(df.loc[df["title"].str.contains(searchIpt)]['title'])[0]
    # 根据精确匹配的片名(searchName)获取对应的评论数据
    # .values[0]获取Series中的第一个值（评论JSON字符串）
    comments = df[df['title'] == searchName]['comments'].values[0]
    comments = json.loads(comments)
    resSrc = getImageByComments(comments)
    # 返回提取的图片资源和匹配的电影名称
    return resSrc, searchName