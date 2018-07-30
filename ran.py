#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
from scipy.stats import norm
import sys
import os
import random
import codecs
import json
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.inf)

def main():

    random_choose()
    draw("0717")

def ransac(chose_data):

    acc = []
    old = 0
    epoch = 500
    num = chose_data.shape[0]
    print(num)

    for n in range(epoch):
        save = []
        random_pick = [random.randint(0, num) for i in range(4)]

        A = np.zeros((8,8))
        b = np.zeros(8)
        for i, k in enumerate(random_pick):
            i = i*2
            x = chose_data[k,1]
            y = chose_data[k,0]
            x_ = chose_data[k,2]
            y_ = chose_data[k,0]

            A[i] = [x, y, 1, 0, 0, 0, -x*x_, -x_*y]
            A[i+1] = [0, 0, 0, x, y, 1, -x*y, -y*y_]
            b[i] = x_
            b[i+1] = y_

        A_out = np.dot(A.T, A)
        print(A_out)
        A_out = np.linalg.inv(A_out)
        h = np.dot(A_out, A.T)
        h = np.dot(h, b.T)
        
        par = 0
        for xy in chose_data:
            x = xy[1]*h[0] + xy[0]*h[1] + h[2] - xy[1]*xy[0]*h[6] - xy[2]*xy[0]*h[7]
            y = xy[0]*h[3] + xy[0]*h[4] + h[5] - xy[1]*xy[0]*h[6] - xy[0]*xy[0]*h[7]

            d = (x-xy[2])**2 + (y-xy[0])**2
            if d < 23000:
                par+=1
                save.append(xy)

        if par > old:
            acc = save
            old = par

    return acc, old

def random_choose():
 
    obj = codecs.open("./parallax/ji_0722.json", 'r', encoding='utf-8').read()
    data = json.loads(obj)
    src = np.array(data)

    h, w = src.shape
    print(src.shape)
    dst = np.copy(src)

    point_src = []
    point_dist = []
    point = []

    for y in range(h):
        for x in range(w):
            if src[y,x]==0:
                continue

            # 任意の画素値を複数の画素値をランダム抽出するために使用
            distance = src[y,x]
            
            point_src.append((y,x))
            point_dist.append((y,x+distance))
            point.append((y,x,x+distance))

    point_src = np.float32(point_src)
    point_dist = np.float32(point_dist)
    point = np.float32(point)

    old = 0
    acc = []

    acc, old = ransac(point)

    img = np.zeros((480,640))
    for t in acc:
        #各座標における
        img[int(t[0]),int(t[1])] = t[2] - t[1]

    ex_json(img)

    
def ex_json(data):

    exp = data.tolist()
    file_path = "./parallax/ji_0722_2.json"

    json.dump(exp, codecs.open(file_path, 'w', encoding='utf-8'), \
              separators=(',', ':'), sort_keys=True, indent=4)
    
    print("------- save array to json -------")


def draw(string):
 
    obj = codecs.open("./parallax/ji_0722_2.json", 'r', encoding='utf-8').read()
    li = json.loads(obj)
    data = np.array(li)

    data = data.astype(np.uint8)

    plt.subplots()
    plt.imshow(data)
    plt.colorbar()
    plt.gray()
    plt.show()

    file_name ="map_" + str(string) + ".png"
    cv2.imwrite(file_name, data)

if __name__ == "__main__":

    main()
