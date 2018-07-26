import cv2
import numpy as np
import glob
import os
import sys

def rotation_and_trans():

  left_rota = np.array([[0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0]])

  left_trans = np.array([[0],
                         [0],
                         [0]])

  right_rota = np.array([[1.0000, -0.0037, 0.0066],
                         [0.00036, 0.9998, 0.0201],
                         [-0.0066, -0.0201, 0.9998]])
   
  right_trans = np.array([[-76.8787],
                          [-1.5949],
                          [9.0437]])

  return left_rota, left_trans, right_rota, right_trans

def in_params():


  """ 内部パラメータとディストーションパラメータ  """
  left_dist = np.array([0.0365, -1.0042, -7.5284e-04, \
                           0.0019, 2.0645])

  right_dist = np.array([-0.0834, -0.1533, 0.0020, \
                            -0.0035, 0.8831])

  left_in_matrix_matlab = np.array([[670.5373, 0, 325.1399],
                                    [0, 669.3633, 241.2748],
                                    [0, 0, 1]])

  right_in_matrix_matlab = np.array([[680.8755, 0, 333.3368],
                                     [0, 682.5116, 256.2893],
                                     [0, 0, 1]])

  return left_in_matrix_matlab, right_in_matrix_matlab, left_dist, right_dist

def calibrate():

  #path = "./../stereo_test/"
  path = "./../block_matching/0718/"
  #path = "./"
  left = "img7_left.jpg"
  right = "img6_right.jpg"

  left_image = os.path.join(path, left) 
  right_image = os.path.join(path, right) 

  left_img = cv2.imread(left_image, 1)
  right_img = cv2.imread(right_image, 1)

  if left_img is None:
    print("-----No Image !!!!!-----")
    sys.exit()

  cam_mat_left, cam_mat_right, dist_left, dist_right = in_params()
  _, _, right_R, right_t = rotation_and_trans()

  # システムの外部パラメータを計算
  imsize = (640, 480)
  
  # 平行化変換のためのRとPおよび3次元変換行列Qを求める
  flag_ = cv2.CALIB_ZERO_DISPARITY
  size_change = -1
  m1type = cv2.CV_32FC1
  
  R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = \
    cv2.stereoRectify(cameraMatrix1=cam_mat_left, distCoeffs1=dist_left, \
                      cameraMatrix2=cam_mat_right, distCoeffs2=dist_right, \
                      imageSize=imsize, \
                      R=right_R, T=right_t, \
                      flags=flag_, alpha=size_change, \
                      newImageSize=imsize)
  
  map1_l, map2_l = cv2.initUndistortRectifyMap(cam_mat_left, dist_left, R2, P1, imsize, m1type)
  map1_r, map2_r = cv2.initUndistortRectifyMap(cam_mat_right, dist_right, R1, P2, imsize, m1type)

  # ReMapにより平行化を行う
  interpolation = cv2.INTER_AREA # INTER_RINEARはなぜか使えない
  left_dst = cv2.remap(left_img, map1_l, map2_l, interpolation)
  #interpolation省略不可
  right_dst = cv2.remap(right_img, map1_r, map2_r, interpolation)

  cv2.imshow("before left", left_img)
  cv2.imshow("before right", right_img)
  cv2.imshow('Rectified Left Target Image', left_dst)
  cv2.imshow('Rectified Right Target Image', right_dst)

  if cv2.waitKey(0)==27:
    cv2.imwrite("Recleft0713_1.png", left_dst)
    cv2.imwrite("Recright0713_1.png", right_dst)
    cv2.destroyAllWindows()

def main():

  calibrate()

if __name__ == '__main__':

  main()
