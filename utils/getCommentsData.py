from .utils import *
import json
import sys
sys.path.append('..')
from word_cloud import *

def getCommentsImage(searchIpt):
    searchName = list(df.loc[df["title"].str.contains(searchIpt)]['title'])[0]
    comments = df[df['title'] == searchName]['comments'].values[0]
    comments = json.loads(comments)
    resSrc = getImageByComments(comments)
    return resSrc, searchName