#!/usr/bin/pyton3
# -*- encoding: utf-8 -*-
import cv2
import subprocess
import sys
import os

class Capture():

    def manual_focus(self):

        try:
            lock_size_left = ['v4l2-ctl', '-d', '/dev/video0', '--set-fmt-video=width=640,height=480']
            subprocess.run(lock_size_left)
      
            lock_size_right = ['v4l2-ctl', '-d', '/dev/video1', '--set-fmt-video=width=640,height=480']
            subprocess.run(lock_size_right)
        
            check_camera = ['v4l2-ctl', '--list-ctrls']
            subprocess.run(check_camera)

        except:
            print("-------v4l2 setup command Error !!!!!--------")
            sys.exit()

    def capture_camera(self):
        cap_left = cv2.VideoCapture(0)
        cap_right = cv2.VideoCapture(1)

        count=0
        while True:
            ret_left, frame_left = cap_left.read()
            ret_right, frame_right = cap_right.read()

            cv2.imshow('left', frame_left)
            cv2.imshow('right', frame_right)

            k = cv2.waitKey(1) 
            if k==115:
                print("----- save image !!! -----")
                cv2.imwrite(os.path.join("./images/", "img" + str(count) + "_left.jpg"), frame_left)
                cv2.imwrite(os.path.join("./images/", "img" + str(count) + "_right.jpg"), frame_right)
                count+=1
            elif k == 27:
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
