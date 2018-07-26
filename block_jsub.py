#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import sys, os, time
import codecs, json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
np.set_printoptions(threshold=np.inf)

# 0 : run all function
# 1 : run plot_graph() only
ch = 0


def RANSAC(ly, lx, rx, bc):

    F = np.array([[5.0584e-08, -1.9910e-05, 0.0027],
                  [2.0863e-05, 3.4542e-06, 0.1049],
                  [-0.0026, -0.1091, 0.5334]])

    ran_num = 0
    for j in range(0, bc):
        for i in range(0, bc):
            left_point = np.array([[lx+i], [ly+j], [1]])
            right_point = np.array([rx+i, ly+j, 1])

            ran1 = np.dot(right_point, F)
            ran2 = np.dot(ran1, left_point)

            ran_num += ran2
    
    ran = ran_num/9

    return ran

def diff_pixel(left, ly, lx, block, step):

    former = left[ly:ly+block,lx:lx+block]
    behind = left[ly:ly+block,lx-step:lx+block-step]

    diff = np.mean(np.abs(former - behind))

    return diff 

def SAD(left, right, ly, lx, rx, block):

    sad = np.sum(np.abs(right[ly:ly+block,rx:rx+block] - left[ly:ly+block,lx:lx+block]))
    
    return sad

def sub_pixel(x_old, x, x_will):
  
    if x_old >= x_will and x_old != x: 
        subpixel = (x_old-x_will) / (2*(x_old-x))
                    
    elif x_old < x_will and x_will != x: 
        subpixel = -1*(x_old-x_will) / (2*(x_will-x))
    else:
        subpixel = 0.0

    return subpixel

def zenbu(left, right):

    start = time.time()

    """
    前提条件 : 基準座標としてる画像->left 比較画像->right
    """
    #画像の大きさ
    h, w = left.shape
    #ブロックの大きさ
    bc = 16
    #ステップ数
    step = 2
    #各ブロックの視差
    diff_x = np.zeros((h, w), dtype=np.float64)

    for ly in range(0, h-bc, step):
        print("------- " + str(ly) + " matching -------")
        
        for lx in range(0, w-bc, step):
            if lx <=50:
                continue
           
            difference = diff_pixel(left, ly, lx, bc, step)
            if lx > step and difference < 0.5:
                diff_x[ly:ly+bc, lx:lx+bc] = diff_x[ly:ly+bc, lx-step:lx+bc-step]
                continue

            bestcost=float(10000)
            for rx in range(1, lx-bc-1, 1):
                cost = SAD(left, right, ly, lx, rx, bc)
                
                if cost < bestcost:
                    bestcost = cost

                    epi = RANSAC(ly, lx, rx, bc)
                    if epi > 15.0 or epi < -15.0:
                        print("!!!!!!!  " + str(epi) + "  !!!!!!!")
                        diff_x[ly:ly+bc, lx:lx+bc] = diff_x[ly:ly+bc, lx-step:lx+bc-step]
                        continue

                    #subpixel推定
                    old = SAD(left, right, ly, lx, rx-1, bc)
                    will = SAD(left, right, ly, lx, rx+1, bc)
                    sub = sub_pixel(old, cost, will)

                    diff_x[ly:ly+bc, lx:lx+bc] = lx-rx + sub

        print(diff_x[ly,lx])
        #print(sub)

    print("------- success caluclate matching !!!!! -------")
    print("bestcost = ", bestcost)
    print("diff = ", diff_x)

    ex_json(diff_x)

    end = time.time() -start

    print("elapased_time:{0}".format(end) + "[sec]")

def ex_json(data):

    exp = data.tolist()
    file_path = "./parallax/ji_0722.json"

    json.dump(exp, codecs.open(file_path, 'w', encoding='utf-8'), \
              separators=(',', ':'), sort_keys=True, indent=4)
    
    print("------- save array to json -------")

def draw(string):
 
    obj = codecs.open("./parallax/ji_0722.json", 'r', encoding='utf-8').read()
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

def calc(data, h, w):

    x, y, z= [], [], []
    x_cood, y_cood, z_cood = 0, 0, 0
    b=70
  
    for j in range(0, h, 1):
        for i in range(0, w, 3):
      
            if data[j,i]==0:
                continue

            else:
                x_cood = ((i-320)*b) / (data[j,i])
                y_cood = -1*((j-240)*b) / (data[j,i])
                z_cood = (670.5373*b) / (data[j,i])
                #x_cood = (320-i)*z_cood/650.6400
                #y_cood = (j-240)*z_cood/650.6400

            if z_cood < 600:
                x.append(x_cood)
                y.append(y_cood)
                z.append(z_cood)
  
    return x, y, z

def plot_graph():
  
    obj = codecs.open("./parallax/ji_0722.json", 'r', encoding='utf-8').read()
    li = json.loads(obj)
    data = np.array(li)

    print(data)
    print(data.shape)
    
    h, w = data.shape

    fig = plt.figure()
    ax = Axes3D(fig)

    x, y, z = calc(data, h, w)
    ax.set_xlabel("x-axis")
    ax.set_ylabel("y-axis")
    ax.set_zlabel("z-axis")

    #座標点を描画
    ax.plot(x, y, z, "o", color="red", ms=0.5, mew=0.4)

    plt.show()

def read():
    
    #im_path = "./images"
    im_path = "./0725/"
    left_im = "img814_left.jpg"
    right_im = "img814_right.jpg"
    #left_im = "mask65_left.png"
    #right_im = "mask65_right.png"
    file_left = os.path.join(im_path, left_im)
    file_right = os.path.join(im_path, right_im)
    
    left = cv2.imread(file_left, 0)
    right = cv2.imread(file_right, 0)
    if left is None:
        print("------- failed read images !!! -------")
        sys.exit()

    #cv2.imshow("ikisugi", left)

    #640*480に画像をresize
    left = cv2.resize(left, (640, 480))
    right = cv2.resize(right, (640, 480))

    kernel = np.array([[-1.0, -1.0, -1.0],
                       [-1.0, 9.0, -1.0],
                       [-1.0, -1.0, -1.0]])

    #kernel = np.array([[-1.0, 0.0, 1.0],
    #                   [-2.0, 0.0, 2.0],
    #                   [-1.0, 0.0, 1.0]])

    left = cv2.filter2D(left, -1, kernel)
    right = cv2.filter2D(right, -1, kernel)

    #left = cv2.fastNlMeansDenoising(left, None, 5, 7)
    #right = cv2.fastNlMeansDenoising(right, None, 5, 7)

    #cv2.imshow("ikisou", left)
    #if cv2.waitKey()==27:
    #    cv2.destroyAllWindows()


    left = cv2.medianBlur(left, 5, (3,3))
    right = cv2.medianBlur(right, 5, (3,3))

    left = np.array(left, dtype=np.float64)
    right = np.array(right, dtype=np.float64)

    return left, right

def main():

    if ch == 0:
        left, right = read()
        zenbu(left, right)
    elif ch == 1:
        draw("0722")
        plot_graph()
    else:
        print("----- Check the number of 'ch' -----")
        sys.exit()

if __name__ == "__main__":

    main()
