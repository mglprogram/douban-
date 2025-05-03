import csv
import json
import os
import random
import re

import numpy as np
import pandas as pd
import pymysql
import requests
from lxml import etree
from pymysql import *
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:root@localhost:3306/dbm')


class spider(object):
    def __init__(self):
        self.session = requests.session()
        self.spiderUrl = 'https://movie.douban.com/j/new_search_subjects'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
        }

    def init(self):
        if not os.path.exists('./tempData.csv'):
            with open('./tempData.csv', 'w', newline='') as w_f:
                # csv自己会处理换行符，若不设置newline，Python会在每行后插入\r\n，导致文件中出现空行
                writer = csv.writer(w_f)
                # 写入表头
                writer.writerow(
                    ['directors', 'title', 'rate', 'actors', 'cover', 'detailLink', 'year', 'types', 'country', 'lang',
                     'time', 'movieTime', 'comment_len', 'stars', 'summary', 'comments', 'imgList', 'movieUrl',
                     'movieUrl_img', 'likeTitle', 'likeCover', 'likeLink'])

        if not os.path.exists('./spiderPage.txt'):
            # 记录当前爬取的页数
            with open('./spiderPage.txt', 'w', encoding='utf-8') as f:
                f.write('0\n')

        try:
            # 连接数据库
            conn = connect(host='localhost', user='root', password='root', database='dbm', port=3306, charset='utf8mb4')
            # 创建movie表
            sql = '''
                                create table movie(
                                    id int primary key auto_increment,
                                    directors varchar(255),
                                    title varchar(255),
                                    rate varchar(255),
                                    actors varchar(255),
                                    cover varchar(255),
                                    detailLink varchar(255),
                                    year varchar(255),
                                    types varchar(255),
                                    country varchar(255),
                                    lang varchar(255),
                                    time varchar(255),
                                    movieTime varchar(255),
                                    comment_len varchar(255),
                                    stars varchar(255),
                                    summary TEXT,
                                    comments TEXT,
                                    imgList TEXT,
                                    movieUrl varchar(255),
                                    movieUrl_img varchar(255),
                                    likeTitle varchar(255),
                                    likeCover varchar(255),
                                    likeLink varchar(255)
                                )DEFAULT CHARSET=utf8mb4;
                        '''
            # 创建游标对象
            cursor = conn.cursor()
            # 执行 SQL 语句
            cursor.execute(sql)
            # 提交事务
            conn.commit()
            print("Table created successfully")
        except pymysql.MySQLError as e:
            print(f"Error creating table: {e}")
            conn.rollback()
        finally:
            # 关闭游标和连接
            cursor.close()
            conn.close()

    # 读取最后一行，即当前页数
    def get_page(self):
        with open('./spiderPage.txt', 'r') as r_f:
            return r_f.readlines()[-1].strip()

    # 写入新的页数
    def set_page(self, newPage):
        with open('./spiderPage.txt', 'a') as w_f:
            w_f.write(str(newPage) + '\n')

    def spiderMan(self, max_pages=100):
        page = self.get_page()
        while int(page) < max_pages:
            params = {
                'start': int(page) * 20
            }
            print(f'正在爬取{int(page) + 1}页')
            respJson = self.session.get(self.spiderUrl, headers=self.headers, params=params).json()
            respJson = respJson['data']
            resultList = []
            # try:
            for index, movieData in enumerate(respJson, start=1):
                print(f"正在爬取第{index}条")
                resultData = []
                # 导演
                resultData.append(','.join(movieData['directors']))
                # 电影名
                resultData.append(movieData['title'])
                # 电影评分
                resultData.append(movieData['rate'])
                # 演员和导演用于是个列表用‘，’隔开
                resultData.append(','.join(movieData['casts']))
                # 封面
                resultData.append(movieData['cover'])
                # 详情链接
                resultData.append(movieData['url'])

                respDetailHTML = self.session.get(movieData['url'], headers=self.headers)
                respDetailHTMLXpath = etree.HTML(respDetailHTML.text)

                # 年份
                try:
                    year = re.findall(r'\d+', respDetailHTMLXpath.xpath('//*[@id="content"]/h1/span[2]/text()')[0])[0]
                    resultData.append(year)
                except:
                    resultData.append(random.randint(1990, 2020))
                # 类型
                types = []
                for i in respDetailHTMLXpath.xpath('//*[@id="info"]/span[@property="v:genre"]'):
                    types.append(i.text)
                resultData.append(','.join(types))
                # 国家
                textInfo = respDetailHTMLXpath.xpath('//*[@id="info"]/text()')
                texts = []
                for i in textInfo:
                    if i.strip() and not i.strip() == "/":
                        texts.append(i)
                try:
                    resultData.append(','.join(texts[0].split(sep='/')))
                except:
                    resultData.append('')
                # 语言
                try:
                    resultData.append(','.join(texts[1].split(sep='/')))
                except:
                    resultData.append('')
                # 上映时间
                try:
                    time = respDetailHTMLXpath.xpath('//*[@id="info"]/span[@property="v:initialReleaseDate"]/@content')[
                               0][
                           :10]
                    resultData.append(time)
                except:
                    timeRandom = (random.randint(2000, 2024), random.randint(1, 12), random.randint(1, 28))
                    time = f"{timeRandom[0]}-{timeRandom[1]}-{timeRandom[2]}"
                    resultData.append(time)
                # 影片时长
                try:
                    movieTime = respDetailHTMLXpath.xpath('//*[@id="info"]/span[@property="v:runtime"]/@content')[0]
                    resultData.append(movieTime)
                # 针对电视剧的
                except:
                    try:
                        resultData.append(re.findAll(r'\d+', texts[4])[0])
                    except:
                        resultData.append(random.randint(31, 69))
                # 短评个数
                try:
                    comment_len = \
                        re.findall(r'\d+',
                                   respDetailHTMLXpath.xpath('//*[@id="comments-section"]/div[1]/h2/span/a/text()')[0])[
                            0]
                    resultData.append(comment_len)
                except:
                    resultData.append(999)
                # 星
                star = respDetailHTMLXpath.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div')
                stars = []
                for i in star:
                    stars.append(i.xpath('./span[@class="rating_per"]/text()')[0])
                resultData.append(','.join(stars))
                # 简介
                try:
                    summary = respDetailHTMLXpath.xpath('//span[@property="v:summary"]/text()')[0].strip()
                    resultData.append(summary)
                except:
                    resultData.append('')
                # 评论
                comments = []
                commentsList = respDetailHTMLXpath.xpath('//*[@id="hot-comments"]/div')
                for i in commentsList:
                    try:
                        user = i.xpath('.//h3/span[@class="comment-info"]/a/text()')[0]
                    except IndexError:
                        user = None  # 或者你可以设置一个默认值
                    # 获取星级评分的class属性
                    star_class = i.xpath('.//h3/span[@class="comment-info"]/span[2]/@class')
                    # 如果star_class为空，则将star设置为0
                    if star_class:
                        try:
                            star = re.findall(r'\d+', star_class[0])[0]
                        except IndexError:
                            star = 40
                    else:
                        star = 40
                    try:
                        times = i.xpath('.//h3/span[@class="comment-info"]/span[3]/@title')[0]
                    except:
                        timesRandom = (
                            random.randint(2000, 2024), random.randint(1, 12), random.randint(1, 28),
                            random.randint(0, 24),
                            random.randint(0, 60), random.randint(0, 60))
                        times = f"{timesRandom[0]}-{timesRandom[1]}-{timesRandom[2]} {timesRandom[3]}:{timesRandom[4]}:{timesRandom[5]}"
                    try:
                        content = i.xpath('.//p[@class="comment-content"]/span/text()')[0]

                    except:
                        content = ''
                    comments.append({
                        'user': user,
                        'star': star,
                        'time': times,
                        'content': content,
                    })
                resultData.append(json.dumps(comments))
                # 图片列表
                imgList = respDetailHTMLXpath.xpath('//ul[contains(@class,"related-pic-bd  ")]//img/@src')
                resultData.append(','.join(imgList))
                # 电影预告片链接
                try:
                    movieUrl = respDetailHTMLXpath.xpath(
                        '//ul[contains(@class,"related-pic-bd  ")]/li[@class="label-trailer"]/a/@href')[0]
                    resultData.append(movieUrl)
                    movieUrl_img = re.findall(r'https?://[^\s)]+',
                                              respDetailHTMLXpath.xpath(
                                                  '//ul[contains(@class,"related-pic-bd  ")]/li[@class="label-trailer"]/a/@style')[
                                                  0])[0]
                    resultData.append(movieUrl_img)
                    # movieHTML = session.get(movieUrl, headers=self.headers)
                    # movieHTMLXpath = etree.HTML(movieHTML.text)
                    # resultData.append(movieHTMLXpath.xpath('//video/source/@src')[0])
                except:
                    resultData.append("无预告片")
                # 同类电影
                like_movies_list = respDetailHTMLXpath.xpath('//*[@id="recommendations"]/div/dl')[:1]
                # like_movies = []
                for dl in like_movies_list:
                    like_movie_title = dl.xpath('./dt/a/img/@alt')[0]
                    like_movie_cover = dl.xpath('./dt/a/img/@src')[0]
                    like_movie_link = dl.xpath('./dt/a/@href')[0]
                    #     like_movies.append({
                    #         'title': like_movie_title,
                    #         'cover': like_movie_cover,
                    #         'link': like_movie_link
                    #     })
                    resultData.append(like_movie_title)
                    resultData.append(like_movie_cover)
                    resultData.append(like_movie_link)
                resultList.append(resultData)
            self.save_to_csv(resultList)
            self.set_page(int(page) + 1)
            self.clear_csv()
            page = self.get_page()  # 更新当前页码
            # spiderObj.spiderMan()  # 继续爬取下一页

    def save_to_csv(self, resultList):
        with open('./tempData.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for rowData in resultList:
                writer.writerow(rowData)

    def clear_csv(self):
        df = pd.read_csv('./tempData.csv')
        # 数据清洗：删除缺失值和重复行
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)
        # 将清洗后的数据写回 CSV 文件
        df.to_csv('./tempData.csv', index=False)
        # 保存到 SQL 数据库
        self.save_to_sql(df)

    def save_to_sql(self, df):
        df.to_sql('movie', con=engine, if_exists='replace', index=False)


if __name__ == '__main__':
    spiderObj = spider()
    # spiderObj.init()
    spiderObj.spiderMan()
    # spiderObj.clear_csv()
