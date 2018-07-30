#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
from scipy.stats import norm
import sys, os
import codecs, json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
np.set_printoptions(threshold=np.inf)

class Plot3D():
    def __init__(self):
        self.json_path = "./parallax/"
        self.json_name = "diff_map.json"
        self.file = str(self.json_path) + str(self.json_name)
        self.data = self.read_json()
        self.h = self.data.shape[0]
        self.w = self.data.shape[1]
        self.string = "plot"

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

        file_name ="map_" + str(iself.string) + ".png"
        cv2.imwrite(file_name, diff)

    def measure(self, glass_point):
  
        glass_point = np.array(glass_point)

        num = glass_point.size
        ave = np.mean(glass_point)
        median = np.median(glass_point)
        dispersion = np.var(glass_point)
        standard = np.std(glass_point)

        X = np.arange(-250,750,0.1)
        Y = norm.pdf(X, ave, standard)

        print("num = ", num)
        print("average = ", ave)
        print("median = ", median)
        print("disperson = ", dispersion)
        print("standard = ", standard)

        fig = plt.figure()
        plt.plot(X, Y, color='g')
        plt.show()

    def calc(self):

        x, y, z= [], [], []
        point = []
        x_cood, y_cood, z_cood = 0, 0, 0
        b=70
        mask = cv2.imread("mask814.png", 0)
        image = cv2.imread("./0725/img814_left.jpg", 1)
        if mask is None or image is None:
            print("----- No mask image or template image in calc -----")
            sys.exit()

        with open("compare.pts", "w") as fp:

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

        return x, y, z

    def plot_graph(self):
  
    
        h, w = self.data.shape

    
        #fig = plt.figure()
        #ax = Axes3D(fig)

        x, y, z = self.calc(h, w)
        '''
        ax.set_xlabel("x-axis")
        ax.set_ylabel("y-axis")
        ax.set_zlabel("z-axis")

        #座標点を描画
        ax.plot(x, y, z, "o", color="red", ms=0.5, mew=0.4)

        plt.show()
        '''

def main():

    draw()
    plot_graph()

if __name__ == "__main__":

    main()
