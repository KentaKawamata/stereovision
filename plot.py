#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
from scipy.stats import norm
import sys
import os
import codecs
import json
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.inf)

class Plot3D():
    def __init__(self):
        self.json_path = "./output/"
        self.json_name = "diff_map.json"
        self.string = "plot"
        self.file = os.path.join(self.json_path, self.json_name)
        self.data = self.read_json()
        self.h = self.data.shape[0]
        self.w = self.data.shape[1]

    def read_json(self):
        obj = codecs.open(self.file, 'r', encoding='utf-8').read()
        li = json.loads(obj)
        data = np.array(li)
        return data

    def draw(self):
 
        diff = self.data.astype(np.uint8)
        plt.subplots()
        plt.imshow(diff)
        plt.colorbar()
        plt.gray()
        plt.show()

        file_name ="map_" + str(self.string) + ".png"
        cv2.imwrite(os.path.join(self.json_path, file_name), diff)

    def measure(self, glass_point):
  
        glass_point = np.array(glass_point)

        num = glass_point.size
        ave = np.mean(glass_point)
        standard = np.std(glass_point)

        X = np.arange(-250,750,0.1)
        Y = norm.pdf(X, ave, standard)

        print("num = ", num)
        print("average = ", ave)
        print("standard = ", standard)

        fig = plt.figure()
        plt.plot(X, Y, color='g')
        plt.show()

    def calc(self):

        x, y, z= [], [], []
        point = []
        x_cood, y_cood, z_cood = 0, 0, 0
        b=70
        mask = cv2.imread("./images/mask814.png", 0)
        image = cv2.imread("./images/img814_left.jpg", 1)
        if mask is None or image is None:
            print("----- No mask image or template image in calc -----")
            sys.exit()

        with open("./output/compare.pts", "w") as fp:

            for j in range(0, self.h, 1):
                for i in range(0, self.w, 3):
                    if self.data[j,i]==0:
                        continue

                    x_cood = -1*((i-320)*b) / (self.data[j,i])
                    y_cood = -1*((j-240)*b) / (self.data[j,i])
                    z_cood = (670.5373*b) / (self.data[j,i])

                    if z_cood < 600:
                        x.append(x_cood)
                        y.append(y_cood)
                        z.append(z_cood)

                        clor = image[j,i]
                        line = "{0} {1} {2} {3} {4} {5}".format(x_cood, y_cood, z_cood, clor[0], clor[1], clor[2])
                        print(line)
                        fp.write(line + "\n")

                        if mask[j,i] == 255:
                            point.append(z_cood)

            self.measure(point)

def main():

    plot = Plot3D()
    plot.draw()
    plot.calc()

if __name__ == "__main__":

    main()
