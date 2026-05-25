import os
import paramiko
import time
import requests
import cv2 as cv
import numpy as np

def try_except(fn):
    def inner(*args,**kwargs):
        try:
            return fn(*args,**kwargs)
        except:
            return -1
    return inner

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
@try_except
def copy_pictures(host, remotepath, dir_window,filename):
    create_dir(dir_window)
    transport = paramiko.Transport((host, 22))
    transport.connect(username="kilox", password="123456")
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.get(remotepath, os.path.join(dir_window,filename))
    transport.close()

def get_picture_name():
    return time.strftime("%Y%m%d%H%M%S")+".jpg"

@try_except
def turnstiles(cmd):
    if cmd:
        requests.post("http://192.168.8.81/awp/TEST/IO_Input.html",data={"Device1":1})
    else:
        requests.post("http://192.168.8.81/awp/TEST/IO_Input.html",data={"Device1":0})

@try_except
def robot_move(socket,cmd, pose):
    socket.sendMsg(
        f"{cmd},{pose[0]},{pose[1]},{pose[2]},"
        f"{pose[3]},{pose[4]},{pose[5]}")
    socket.recvMsg()

def getCenterRealsense(file):
    value_low=350
    value_high=3000
    hsv_low=[100, 43, 46]
    hsv_high=[124, 255, 255]
    img = cv.imread(file)
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    low = np.array(hsv_low)
    high = np.array(hsv_high)
    im1 = cv.inRange(hsv, low, high)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (7, 7))
    er = cv.erode(im1, kernel,iterations=2)
    dil = cv.dilate(er, kernel,iterations=2)
    ctns, ah = cv.findContours(dil, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    cx = cy  = 0
    for ct in ctns:
        print(cv.arcLength(ct, True))
        if value_low < cv.arcLength(ct, True) < value_high:
            M=cv.moments(ct)
            cx=int(M["m10"]/M["m00"])
            cy = int(M["m01"] / M["m00"])
            #cv.circle(img, (cx, cy), 2, (0, 255, 0), 2)
            #cv.imshow("11",img)
            #cv.waitKey()
    return cx, cy

def RealsenseRecongnize(file):
    return  getCenterRealsense(file)







