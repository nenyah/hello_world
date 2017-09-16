# -*- coding: utf-8 -*-
# @Author: steven
# @Date:   2017-09-02 16:40:40
# @Last Modified by:   steven
# @Last Modified time: 2017-09-02 16:40:59
from pyecharts import Bar

bar = Bar("我的第一个图表", "这里是副标题")
bar.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90])
bar.show_config()
bar.render()
