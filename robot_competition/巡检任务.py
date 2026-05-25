import cv2


from roslib.rosbase import *
from roslib.hk_ptz_camera import *


def main():
    ros = RosBase('192.168.8.11', 51848)
    ros.rosConnect()
    time.sleep(0.5)

    #导航到面板前
    ros.moveToPose([2.03786, -0.03003, -0.02712])


    #############视觉检测###########
    #云台相机初始化
    cam = HKPTZCamera()
    cam.init()
    #拍照
    ret, frame = cam.snap()
    #调用yolo检测
    if ret:
        dst = cv2.resize(frame, (680, 480))
        cv2.imshow('src', dst)
        cv2.waitKey(100)

    #导航回home点
    ros.moveToPose([0.30814, 0.06207, -0.02294])
    ros.rosClose()



if __name__ == '__main__':
    main()