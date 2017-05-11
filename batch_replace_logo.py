#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-

from PIL import Image
import os
import re
from multiprocessing import Pool


def removeLogo(img):
    if os.path.exists(img):
        im = Image.open(img)
        width, height = im.size
        if height / width > 0.875:
            box = (0, 0, 220, 220)
            roi = im.crop(box)
            roi = roi.point(lambda i: i**0 * 255)

            layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
            layer.paste(roi, (0, 0))
            out = Image.composite(layer, im, layer)
            out.save(img)
        else:
            print("Needn't remove")
    else:
        print("File doesn't exists!!")


def addLogo(img):
    im = Image.open(img)

    logo_img = r"C:\Users\steve\Desktop\Temp\商标logo\MOVEFUN.png"
    logo = Image.open(logo_img)
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    layer.paste(logo, (0, 0))
    out = Image.composite(layer, im, layer)
    out.save(img)


def makePath(root):
    imgs = []
    fileNumber = os.listdir(root)
    paths = [r"{0}{1}\pImg".format(root, path) for path in fileNumber]
    for path in paths:
        for file in os.listdir(path):
            imgs.append(os.path.join(path, file))
    return imgs


if __name__ == '__main__':
    path = r"C:\Users\steve\Desktop\0"
    imgs = makePath(path)
    # print(imgs)
    # p = Pool()
    # p.map(removeLogo, imgs)
    # p.close()
    # p.join()
    ad_imgs = [re.findall(r".*\\PImg1_.*", img)[0]
               for img in imgs
               if re.findall(r".*\\PImg1_.*", img)]
    print(ad_imgs)

    p = Pool()
    p.map(addLogo, ad_imgs)
    p.close()
    p.join()
