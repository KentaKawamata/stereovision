#!/usr/bin/pyton3
# -*- encoding: utf-8 -*-
import cv2
import subprocess, sys
import os

class Capture():

  def manual_focus(self):

    try:
        #kill_autofocus_left = ['v4l2-ctl', '-d', '/dev/video0', '-c', 'focus_auto=0']
        #subprocess.run(kill_autofocus_left)
        #set_focus_left = ['v4l2-ctl', '-d', '/dev/video0', '-c', 'focus_absolute=100']
        #subprocess.run(set_focus_left)
        
        #kill_white_balance_left = ['v4l2-ctl', '-d', '/dev/video0', \
        #                           '--set-ctrl=white_balance_temperature_auto=0']
        #subprocess.run(kill_white_balance_left)
        #lock_gain_left = ['v4l2-ctl', '-d', '/dev/video0', '--set-ctrl=gain=30']
        #subprocess.run(lock_gain_left)
        #lock_color_table_left = ['v4l2-ctl', '-d', '/dev/video0', '--set-ctrl=white_balance_temperature=5000']
        #subprocess.run(lock_color_table_left)
        #lock_exposure_left = ['v4l2-ctl', '-d', '/dev/video0', '-c', 'exposure_auto=1']
        #subprocess.run(lock_exposure_left)
        lock_size_left = ['v4l2-ctl', '-d', '/dev/video0', '--set-fmt-video=width=640,height=480']
        subprocess.run(lock_size_left)
      


        #right
        #kill_autofocus_right = ['v4l2-ctl', '-d', '/dev/video1', '-c', 'focus_auto=0']
        #subprocess.run(kill_autofocus_right)
        #set_focus_right = ['v4l2-ctl', '-d', '/dev/video1', '-c', 'focus_absolute=100']
        #subprocess.run(set_focus_right)
        
        #kill_white_balance_right = ['v4l2-ctl', '-d', '/dev/video1', \
        #                            '--set-ctrl=white_balance_temperature_auto=0']
        #subprocess.run(kill_white_balance_right)
        #lock_gain_right = ['v4l2-ctl', '-d', '/dev/video1', '--set-ctrl=gain=30']
        #subprocess.run(lock_gain_right)
        #lock_color_table_right = ['v4l2-ctl', '-d', '/dev/video1', '--set-ctrl=white_balance_temperature=5000']
        #subprocess.run(lock_color_table_right)
        #lock_exposure_right = ['v4l2-ctl', '-d', '/dev/video1', '-c', 'exposure_auto=1']
        #subprocess.run(lock_exposure_right)
        lock_size_right = ['v4l2-ctl', '-d', '/dev/video1', '--set-fmt-video=width=640,height=480']
        subprocess.run(lock_size_right)
        
        check_camera = ['v4l2-ctl', '--list-ctrls']
        subprocess.run(check_camera)

    except:
        print("-------v4l2 setup command Error !!!!!--------")
        sys.exit()

  def capture_camera(self):

    # カメラをキャプチャする
    cap_left = cv2.VideoCapture(0)
    cap_right = cv2.VideoCapture(1)

    count=1000
    while True:
        ret_left, frame_left = cap_left.read()
        ret_right, frame_right = cap_right.read()

        cv2.imshow('left', frame_left)
        cv2.imshow('right', frame_right)

        k = cv2.waitKey(1) 

        if k==115:
            print("----- save image !!! -----")
            cv2.imwrite(os.path.join("./stereocalib/", "img" + str(count) + "_left.jpg"), frame_left)
            cv2.imwrite(os.path.join("./stereocalib/", "img" + str(count) + "_right.jpg"), frame_right)
            count+=1

        if k == 27:
            break

    cap_left.release()
    cap_right.release()
    cv2.destroyAllWindows()

  def capture(self):
    self.manual_focus()
    self.capture_camera()

def main():

  cap = Capture()
  cap.capture()

if __name__ == "__main__":

  main()
