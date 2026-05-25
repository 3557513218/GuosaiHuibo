import time
import yaml
import os
from PySide6.QtCore import QThread, Slot, Signal
from hk_ptz_camera import *

class CameraClient(QThread):
    signal_int = Signal(str)  # 定义信号连接状态
    signal_img = Signal()     # 信号 图像更新

    __cam = None
    is_connect = False      #连接状态
    image = None            #全局图像
    is_run = True

    def __init__(self):
        super().__init__()
        self.is_connect = False

        #加载yaml参数文件
        curPath = os.path.dirname(os.path.realpath(__file__))
        ymlPath = os.path.join(curPath, "config.yaml")
        # print(ymlPath)
        try:
            with open(ymlPath, 'r', encoding='utf-8') as f:
                msg = yaml.load(f, Loader=yaml.FullLoader)
                # print(msg)
                self.__cam = HKPTZCamera(msg['camera']['ip'], msg['camera']['user'],msg['camera']['password'])
        except Exception as e:
            #默认参数初始化 未找到配置文件
            self.__cam = HKPTZCamera()
            print(e)
    def move(self, x, y):
        if self.is_connect:
            self.__cam.absMove(x, y)

    def stop(self):
        self.is_run = False

    def run(self):
        self.is_run = True
        self.signal_int.emit('连接中,请稍等...')
        #print('camera start init...')
        #初始化相机
        ret = self.__cam.init()
        if ret == -1:
            print('init camera error!')
            self.signal_int.emit('连接相机超时!')
            return
        is_open = self.__cam.open()
        if not is_open:
            print('open rtsp stream error!')
            self.signal_int.emit('连接相机超时!')
            return
        self.signal_int.emit('已连接')
        self.is_connect = True
        while self.is_run:
            ret, self.image = self.__cam.read()
            if ret:
                self.signal_img.emit()
                # cv2.imshow('src', frame)
                # print('111')
                # cv2.waitKey(1)
            time.sleep(0.01)

        self.signal_int.emit('未连接')
        self.is_connect = False





