#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import sys, os, time
import codecs, json
import numpy as np
np.set_printoptions(threshold=np.inf)

class TemplateMatching():
    def __init__(self, left_img, right_img):
        self.left = left_img
        self.right = right_img
        self.block = 16
        self.step = 2
        self.json_path = "./output/"
        self.json_name = "diff_map.json"

    def fundamental(self, ly, lx, rx):

        F = np.array([[5.0584e-08, -1.9910e-05, 0.0027],
                      [2.0863e-05, 3.4542e-06, 0.1049],
                      [-0.0026, -0.1091, 0.5334]])

        ran_num = 0
        for j in range(0, self.block):
            for i in range(0, self.block):
                left_point = np.array([[lx+i], [ly+j], [1]])
                right_point = np.array([rx+i, ly+j, 1])

                ran1 = np.dot(right_point, F)
                ran2 = np.dot(ran1, left_point)

                ran_num += ran2
    
        ran = ran_num/9

        return ran

    def diff_pixel(self, ly, lx):

        bc = self.block
        st = self.step

        former = self.left[ly:ly+bc,lx:lx+bc]
        behind = self.left[ly:ly+bc,lx-st:lx+bc-st]

        diff = np.mean(np.abs(former - behind))

        return diff 

    def SAD(self, ly, lx, rx):

        bc = self.block
        sad = np.sum(np.abs(self.right[ly:ly+bc,rx:rx+bc] - self.left[ly:ly+bc,lx:lx+bc]))
    
        return sad

    def sub_pixel(self, x_old, x, x_will):
  
        if x_old >= x_will and x_old != x: 
            subpixel = (x_old-x_will) / (2*(x_old-x))
                    
        elif x_old < x_will and x_will != x: 
            subpixel = -1*(x_old-x_will) / (2*(x_will-x))
        else:
            subpixel = 0.0

        return subpixel

    def matching(self):

        start = time.time()
        bc = self.block
        step = self.step
        h, w = self.left.shape
        diff_x = np.zeros((h, w), dtype=np.float64)

        for ly in range(0, h-bc, step):
            print("------- " + str(ly) + " matching -------")
        
            for lx in range(0, w-bc, step):
                if lx <=50:
                    continue
           
                diff = self.diff_pixel(ly, lx)
                if lx > step and diff < 0.5:
                    diff_x[ly:ly+bc, lx:lx+bc] = diff_x[ly:ly+bc, lx-step:lx+bc-step]
                    continue

                bestcost=float(10000)
                for rx in range(1, lx-bc-1, 1):
                    cost = self.SAD(ly, lx, rx)
                
                    if cost < bestcost:
                        bestcost = cost

                        epi = self.fundamental(ly, lx, rx)
                        if epi > 15.0 or epi < -15.0:
                            print("!!!!!!!  " + str(epi) + "  !!!!!!!")
                            diff_x[ly:ly+bc, lx:lx+bc] = diff_x[ly:ly+bc, lx-step:lx+bc-step]
                            continue

                        #subpixel推定
                        old = self.SAD(ly, lx, rx-1)
                        will = self.SAD(ly, lx, rx+1)
                        sub = self.sub_pixel(old, cost, will)

                        diff_x[ly:ly+bc, lx:lx+bc] = lx-rx + sub


        print("------- success caluclate matching !!!!! -------")
        print("bestcost = ", bestcost)
        print("diff = ", diff_x)

        self.ex_json(diff_x)

        end = time.time() -start

        print("elapased_time:{0}".format(end) + "[sec]")

    def ex_json(self, data):

        exp = data.tolist()
        file_path = str(json_path) + str(self.json_name)

        json.dump(exp, codecs.open(file_path, 'w', encoding='utf-8'), \
                  separators=(',', ':'), sort_keys=True, indent=4)
    
        print("------- save array to json -------")

def read():
    im_path = "./0725/"
    left_im = "img814_left.jpg"
    right_im = "img814_right.jpg"
    file_left = os.path.join(im_path, left_im)
    file_right = os.path.join(im_path, right_im)
    
    left = cv2.imread(file_left, 0)
    right = cv2.imread(file_right, 0)
    if left is None:
        print("------- failed read images !!! -------")
        sys.exit()

    kernel = np.array([[-1.0, -1.0, -1.0],
                       [-1.0, 9.0, -1.0],
                       [-1.0, -1.0, -1.0]])

    left = cv2.filter2D(left, -1, kernel)
    right = cv2.filter2D(right, -1, kernel)

    #left = cv2.fastNlMeansDenoising(left, None, 5, 7)
    #right = cv2.fastNlMeansDenoising(right, None, 5, 7)

    left = cv2.medianBlur(left, 5, (3,3))
    right = cv2.medianBlur(right, 5, (3,3))

    left = np.array(left, dtype=np.float64)
    right = np.array(right, dtype=np.float64)

    return left, right

def main():

    left, right = read()
    TemplateMatching(left, right)
    TemplateMatching.matching()

if __name__ == "__main__":

    main()
