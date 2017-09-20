#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-

from PIL import Image
import os
import re
from multiprocessing import Pool
import sys


def remove_logo(img):
    print("Try to remove {}".format(img))
    if os.path.exists(img):
        im = Image.open(img)
        width, height = im.size
        if height / width > 0.875:
            box = (0, 0, 220, 230)
            roi = im.crop(box)
            roi = roi.point(lambda i: i**0 * 255)

            layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
            layer.paste(roi, (0, 0))
            out = Image.composite(layer, im, layer)
            out.save(img)
            return True
        else:
            print("Needn't remove")
            return False
    else:
        print("File doesn't exists!!")
        return False


def replace_logo(img, logo="robesbon"):
    print("Try to replace {} logo to {}".format(logo, img))
    result = remove_logo(img)
    if result:
        im = Image.open(img)
        width, height = im.size
        logo_img = r"E:\Work\06-Work\09-企业相关\商标logo\{}.png".format(logo)
        logo = Image.open(logo_img)
        layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
        layer.paste(logo, (0, 0))
        out = Image.composite(layer, im, layer)
        out.save(img)


def makePath(root, keypath=None, keyword=None):
    imgs = []
    for info in os.walk(root):
        for file in info[-1]:
            imgs.append(os.path.join(info[0], file))
    return [img for img in imgs if keyword in img]


if __name__ == '__main__':
    print(sys.argv, len(sys.argv))
    if len(sys.argv) == 3:
        path = sys.argv[-1]
    elif len(sys.argv) == 5:
        path = sys.argv[-3]
        logo = sys.argv[-1]
    else:
        print(
            "Lack enough order!!!\nthe correct order should be: \nptyhon batch_replace_logo.py -p path [-n logo_name]")
        sys.exit()

    imgs = makePath(path, keyword='pImg')

    p = Pool()
    for img in imgs:
        if logo:
            p.apply_async(replace_logo, args=(img, logo))
        else:
            p.apply_async(replace_logo, args=(img, ))
    p.close()
    p.join()
