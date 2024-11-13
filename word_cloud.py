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

def generate_wordcloud(text, target_image, res_image):
    # 分词
    cut = jieba.cut(text)
    string = ' '.join(cut)

    # 读取目标图像
    img = Image.open(target_image)
    img_arr = np.array(img)

    # 生成词云
    wc = WordCloud(
        background_color='white',
        mask=img_arr,
        font_path='STHUPO.TTF'  # 使用指定的字体文件
    )
    wc.generate_from_text(string)

    # 绘图
    plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')

    # 保存图像
    plt.savefig(res_image)

def getImageByComments(comments):
    text = ''.join(comment['content'] for comment in comments)
    random_int = random.randint(1, 100000000)
    res_image = f'static/wordcloudImage/{random_int}.png'
    generate_wordcloud(text, 'static/word.png', res_image)
    return res_image

def getImageByAuthor(field, target_image, res_image):
    sql = f'SELECT {field} FROM movie'
    data = querys(sql, [], 'select')
    text = ''.join(item[0] for item in data)
    generate_wordcloud(text, target_image, res_image)

def getImageByActors(target_image, res_image):
    actors_list = typeList('actors')
    text = ''.join(actors_list)
    generate_wordcloud(text, target_image, res_image)

# 示例调用
getImageByActors('./static/word4.png', './static/wordcloudImage/actors_cloud.png')
