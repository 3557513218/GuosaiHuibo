import time

import cv2
import requests
from utils import try_except
from func_timeout import  func_set_timeout

base_url_songling="http://192.168.8.32:5000/"
base_url_hb="http://192.168.8.21:5001/"

class SongLingCar():
    @staticmethod
    @try_except
    def moveToPose(pose,cmd="start",speed=0.5):
        url=base_url_songling+"moveToPose"
        data={
            "x":pose[0],
            "y": pose[1],
            "yaw": pose[2],
            "cmd":cmd,
            "speed":speed
        }
        return requests.post(url=url,data=data,timeout=3).json()


    @staticmethod
    @try_except
    def getNavigationState():
        url = base_url_songling+"getNavigationState"
        return requests.get(url=url,timeout=3).json()


    @staticmethod
    @try_except
    def manualMove(speed_x,speed_yaw):
        url = base_url_songling + "manualMove"
        data = {
            "x": speed_x,
            "yaw": speed_yaw
        }
        return requests.get(url=url, params=data,timeout=3).json()


    @staticmethod
    @try_except
    def usbCamera(image_name):
        url = base_url_songling+"usbCamera"
        data={
            "image_name":image_name
        }
        return requests.get(url=url,params=data,timeout=3).json()

class HbCar():
    @staticmethod
    @try_except
    def moveToPose(pose, cmd="new"):
        url = base_url_hb + "moveToPose"
        data = {
            "x": pose[0],
            "y": pose[1],
            "yaw": pose[2],
            "cmd": cmd
        }
        return requests.get(url=url, params=data, timeout=3).json()

    @staticmethod
    @try_except
    def manualMove(speed_x, speed_yaw):
        url = base_url_hb + "manualMove"
        data = {
            "x": speed_x,
            "yaw": speed_yaw
        }
        return requests.get(url=url, params=data, timeout=3).json()

    @staticmethod
    @try_except
    def getNavigationState():
        url = base_url_hb + "getNavigationState"
        return requests.get(url=url, timeout=3).json()

    @staticmethod
    @try_except
    def realsenseCamera(cmd):
        url = base_url_hb + "realsense"
        data = {
            "cmd": cmd
        }
        res= requests.get(url=url, params=data, timeout=5).json()
        if res["error_code"]==0:
            return res["result"]
        else:
            raise ValueError

if __name__ == '__main__':
    print(HbCar.getNavigationState())
    # HbCar.moveToPose()
    # print(HbCar.realsenseCamera(1))
    # HbCar.manualMove(0.2,0)
    # time.sleep(2)
    # HbCar.manualMove(0,0)
    print(HbCar.moveToPose([1.8,0.6,-2.8]))