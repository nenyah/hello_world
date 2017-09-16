import itchat
import os

import PIL.Image as Image
from os import listdir
import math

itchat.auto_login()

friends = itchat.get_friends(update=True)[0:]

user = friends[0]["UserName"]

full_path = f'F:\{user}'
if not os.path.exists(full_path):
    os.mkdir(full_path)  # 为自己创建一个文件夹

os.chdir(full_path)  # 切换路径

num = 0

for i in friends:
    img = itchat.get_head_img(userName=i["UserName"])
    with open(str(num) + ".jpg", 'wb') as f:
        f.write(img)
    num += 1

pics = listdir('.')

numPic = len(pics)

print(numPic)

eachsize = int(math.sqrt(float(640 * 640) / numPic))

print(eachsize)

numline = int(640 / eachsize)

toImage = Image.new('RGBA', (640, 640))


print(numline)

x = 0
y = 0

for i in pics:
    try:
        # 打开图片
        img = Image.open(i)
    except IOError:
        print("Error: 没有找到文件或读取文件失败")
    else:
        # 缩小图片
        img = img.resize((eachsize, eachsize), Image.ANTIALIAS)
        # 拼接图片
        toImage.paste(img, (x * eachsize, y * eachsize))
        x += 1
        if x == numline:
            x = 0
            y += 1


toImage.save(user + ".jpg")


itchat.send_image(user + ".jpg", 'filehelper')
