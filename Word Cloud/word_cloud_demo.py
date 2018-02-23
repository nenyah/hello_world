#!/usr/bin/env python
# coding:utf-8
__author__ = 'Steven Tan'

import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from os import path
from scipy.misc import imread
import shutil
from pathlib import Path


def get_file_names(path, pedix=None):
    """get all file name in path"""
    p = Path(path)
    if pedix:
        return p.glob(f'**/*.{pedix}*')
    return p.glob(f'**/*.*')


file = r"E:\workspace\儒道至圣"
# for path in get_file_names(file):
#     with open(path,'r', encoding='utf-8') as f:
#         content = f.read()
#     with open(r'E:\workspace\total.txt','a+', encoding='utf-8') as f:
#         f.write(content)
#         f.write('\n')
#     print(path)

# 当前目录
d = path.dirname(__file__)


delwords = '【大家可以好好的看书，但是要注意研究休息哦，我们的网站更新最快最好，免费无弹窗广告，热血小说网：www.xieyixs.com，百度xieyixs就可以了】'
segments = []
file = r"E:\workspace\total.txt"
with open(file, 'r', encoding='utf-8') as f:
    content = f.read().replace(delwords, '')
    content = content.replace('方运道', '方运')
    # print(content)
    segs = jieba.cut(content)
    segments = [seg for seg in segs if len(seg) > 1]
    # print(segments)
    new_text = ' '.join(segments)


# 设置背景图片
back_coloring = imread(path.join(d, "./image/mask.jpg"))

wordcloud = WordCloud(
    font_path=r"./fonts/MSYH.TTF",  # 设置字体
    background_color="white",  # 背景颜色
    max_words=2000,  # 词云显示的最大词数
    mask=back_coloring,  # 设置背景图片
    max_font_size=100,  # 字体最大值
    random_state=42,
).generate(new_text)

plt.figure()
# 显示图片
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
plt.close()

# 保存图片
wordcloud.to_file(path.join(d, "儒道至圣1.png"))
