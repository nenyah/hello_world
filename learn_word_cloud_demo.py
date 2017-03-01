# coding:utf-8
__author__ = 'Steven Tan'

import jieba
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud

delwords = '【大家可以好好的看书，但是要注意研究休息哦，我们的网站更新最快最好，免费无弹窗广告，热血小说网：www.xieyixs.com，百度xieyixs就可以了】'
segments = []
with open(r"F:\hello_world\content-c.txt",'r') as f:
	content = f.read().replace(delwords,'')
	# print(content)
	segs = jieba.cut(content)
	segments = [seg for seg in segs if len(seg) > 1]
	# print(segments)
segmentDF = pd.DataFrame({'segments':segments})

segStat = segmentDF['segments'].value_counts()
# .agg({'计数':np.size}).reset_index().sort_value(by=['计数'], ascending=False)
# wordcloud = WordCloud(font_path=r"./fonts/MSYH.TTF",background_color="white")
# wordcloud = wordcloud.fit_words(segStat.head(500)) 
# plt.figure(num=None, figsize=(15,14), dpi=800, facecolor='w', edgecolor='k')
# plt.imshow(wordcloud)
# plt.axis("off")
# plt.show()
# plt.close()
print(segStat.head(500))