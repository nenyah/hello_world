# -*- coding: utf-8 -*-
# @Author: steven
# @Date:   2017-09-01 09:55:44
# @Last Modified by:   steven
# @Last Modified time: 2017-09-01 10:26:08
import itchat
import numpy as np
import pandas as pd
from collections import defaultdict
import re
import jieba
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import PIL.Image as Image

itchat.login()
friends = itchat.get_friends(update=True)

NickName = friends[0].NickName  # 获取自己的昵称
full_path = f'F:\{NickName}'
if not os.path.exists(full_path):
    os.mkdir(full_path)  # 为自己创建一个文件夹

os.chdir(full_path)  # 切换路径

number_of_friends = len(friends)
df_friends = pd.DataFrame(friends)
df_friends.to_csv('frends.csv', index=False)


def get_count(Sequence):
    counts = defaultdict(int)  # 初始化一个字典
    for x in Sex:
        counts[x] += 1
    return counts

Sex = df_friends.Sex
Sex_count = get_count(Sex)
Sex_count = Sex.value_counts()
Sex_count.plot(kind='bar')

Province = df_friends.Province
Province_count = Province.value_counts()
Province_count = Province_count[Province_count.index != '']

City = df_friends.City
City_count = City.value_counts()
City_count = City_count[City_count.index != '']

file_name_all = NickName + '_basic_inf.txt'

with open(file_name_all, 'w') as f:
    f.write(
        '你共有%d个好友,其中有%d个男生，%d个女生，%d未显示性别。\n\n' % (number_of_friends, Sex_count[1], Sex_count[2], Sex_count[0]) + '你的朋友主要来自省份：%s(%d)、%s(%d)和%s(%d)。\n\n' % (Province_count.index[0], Province_count[
            0],
            Province_count.index[
            1],
            Province_count[
            1],
            Province_count.index[
            2],
            Province_count[
            2]
        ) + '主要来自这些城市：%s(%d)、%s(%d)、%s(%d)、%s(%d)、%s(%d)和%s(%d)。' % (
            City_count.index[0],
            City_count[0],
            City_count.index[1],
            City_count[1],
            City_count.index[2],
            City_count[2],
            City_count.index[3],
            City_count[3],
            City_count.index[4],
            City_count[4],
            City_count.index[5],
            City_count[5])
    )
Signatures = df_friends.Signature
regex1 = re.compile('<span.*?</span>')  # 匹配表情
regex2 = re.compile('\s{2,}')  # 匹配两个以上占位符。
Signatures = [regex2.sub(' ', regex1.sub('', signature, re.S))
              for signature in Signatures]  # 用一个空格替换表情和多个空格。
Signatures = [signature for signature in Signatures if len(
    signature) > 0]  # 去除空字符串
text = ' '.join(Signatures)
file_name = NickName + '_wechat_signatures.txt'
with open(file_name, 'w', encoding='utf-8') as f:
    f.write(text)
wordlist = jieba.cut(text, cut_all=True)
word_space_split = ' '.join(wordlist)
# 词云的背景和颜色。这张图片在本地。
coloring = np.array(Image.open("../learn word cloud/image/mask.png"))

my_wordcloud = WordCloud(background_color="white",
                         max_words=2000,
                         mask=coloring,
                         max_font_size=60,
                         random_state=42,
                         scale=2,
                         font_path="C:\Windows\Fonts\msyhl.ttc").generate(word_space_split)

file_name_p = NickName + '.jpg'
my_wordcloud.to_file(file_name_p)
