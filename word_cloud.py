# import jieba
# from PIL import Image
# import numpy as np
# from matplotlib import pyplot as plt
# from wordcloud import WordCloud
# import random
# from utils.query import querys
# from utils.utils import typeList
#
#
# def getImageByComments(comments):
#     text = ''
#     for i in comments:
#         text = text + i['content']
#
#     # 分词
#     cut = jieba.cut(text)
#     string = ' '.join(cut)
#
#     img = Image.open('static/word.png')
#     img_arr = np.array(img)
#     wc = WordCloud(
#         background_color='white',
#         mask=img_arr,
#         font_path='STHUPO.TTF'
#     )
#     wc.generate_from_text(string)
#
#     # 绘图
#     flg = plt.figure(1)
#     plt.imshow(wc)
#     plt.axis('off')
#
#     randomInt = random.randint(1, 100000000)
#     plt.savefig(f'static/wordcloudImage/{randomInt}.png')
#     return f'static/wordcloudImage/{randomInt}.png'
#
# def getImageByAuthor(field,targetImage,resImage):
#     sql = 'select {} from movie'.format(field)
#     data = querys(sql,[],'select')
#     text = ''
#     for i in data:
#         text = text + i[0]
#
#     # 分词
#     cut = jieba.cut(text)
#     string = ' '.join(cut)
#
#     img = Image.open(targetImage)
#     img_arr = np.array(img)
#     wc = WordCloud(
#         background_color='white',
#         mask=img_arr,
#         font_path='STHUPO.TTF'
#     )
#     wc.generate_from_text(string)
#
#     # 绘图
#     flg = plt.figure(1)
#     plt.imshow(wc)
#     plt.axis('off')
#
#     randomInt = random.randint(1, 100000000)
#     plt.savefig(resImage)
#
#
# def getImageByActors(targetImage,resImage):
#     actorsList = typeList('actors')
#     text = ''
#     for i in actorsList:
#         text = text + i
#
#     # 分词
#     cut = jieba.cut(text)
#     string = ' '.join(cut)
#
#     img = Image.open(targetImage)
#     img_arr = np.array(img)
#     wc = WordCloud(
#         background_color='white',
#         mask=img_arr,
#         font_path='STHUPO.TTF'
#     )
#     wc.generate_from_text(string)
#
#     # 绘图
#     flg = plt.figure(1)
#     plt.imshow(wc)
#     plt.axis('off')
#
#     randomInt = random.randint(1, 100000000)
#     plt.savefig(resImage)
#
#
# getImageByActors('./static/word4.png','./static/wordcloudImage/actors_cloud.png')

import jieba
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from wordcloud import WordCloud
import random
from utils.query import querys
from utils.utils import typeList


# 生成词云图片并保存
def generate_wordcloud(text, target_image, res_image):
    # 使用jieba进行中文分词，结果用空格连接成字符串
    cut = jieba.cut(text)
    string = ' '.join(cut)

    # 读取模板图片并转为NumPy数组（用于定义词云形状）
    img = Image.open(target_image)
    img_arr = np.array(img)

    # 配置词云参数
    wc = WordCloud(
        background_color='white',
        mask=img_arr,  # 形状模板
        font_path='STHUPO.TTF'  # 中文字体路径（避免乱码）
    )
    wc.generate_from_text(string)  # 从文本生成词云

    # 绘图
    plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')

    # 保存图像
    plt.savefig(res_image)


# 从评论数据生成词云图片
def getImageByComments(comments):
    # 将所有评论内容拼接成一个字符串
    text = ''.join(comment['content'] for comment in comments)
    # 生成随机文件名（避免重复）
    random_int = random.randint(1, 100000000)
    res_image = f'static/wordcloudImage/{random_int}.png'
    generate_wordcloud(text, 'static/resource_img/word5.png', res_image)
    return res_image


# 从指定字段生成词云图片
def getImageByAuthor(field, target_image, res_image):
    # 从数据库查询指定字段的所有数据
    sql = f'SELECT {field} FROM movie'
    data = querys(sql, [], 'select')  # 数据库查询函数
    # 拼接所有字段值为一个字符串
    text = ''.join(item[0] for item in data)
    generate_wordcloud(text, target_image, res_image)


# 从演员列表生成词云
def getImageByActors(target_image, res_image):
    # 获取所有演员列表（假设typeList返回演员名字列表）
    actors_list = typeList('actors')
    text = ''.join(actors_list)
    generate_wordcloud(text, target_image, res_image)


# 演员词云
# getImageByActors('./static/resource_img/word4.png', './static/wordcloudImage/actors_cloud.png')
# 标题词云
# getImageByAuthor('title','./static/resource_img/word3.png', './static/wordcloudImage/title_cloud.png')
# 导演词云
# getImageByAuthor('summary','./static/resource_img/word.png', './static/wordcloudImage/summary_cloud.png')