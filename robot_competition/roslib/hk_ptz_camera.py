from roslib.utils import try_except
import cv2 as cv
from onvif import ONVIFCamera
import os

"""
    海康云台相机接口
2024-10-09 huibo.robot
"""

class HKPTZCamera:
    def __init__(self, ip='192.168.8.12', user='admin', password='kilox1234'):
        self.__ip= ip
        self.__user = user
        self.__password = password
        self.inited = False

    @try_except
    def init(self):
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        wsdl_dir = os.path.join(curr_dir, 'wsdl')
        print('wdsl_path: ', wsdl_dir)
        print('初始化云台相机. ip:{} user:{} password:{}'.
              format(self.__ip, self.__user, self.__password))
        self.cam = ONVIFCamera(self.__ip, 80, self.__user, self.__password, wsdl_dir=wsdl_dir)
        self.media = self.cam.create_media_service()
        self.profile = self.media.GetProfiles()[0]
        self.imaging = self.cam.create_imaging_service()
        self.inited = True




    def open(self):
        self.__cap = cv.VideoCapture(
            'rtsp://{}:{}@{}:554/Streaming/Channels/101'.
            format(self.__user, self.__password, self.__ip))
        return self.__cap.isOpened()

    @try_except
    def read(self):
        return self.__cap.read()

    def close(self):
        self.__cap.release()

    #拍照 返回图片
    @try_except
    def snap(self):
        cap = cv.VideoCapture(
            'rtsp://{}:{}@{}:554/Streaming/Channels/101'.
            format(self.__user, self.__password, self.__ip))
        ret, frame = cap.read()
        cap.release()
        return ret, frame

    #拍照 保存图片
    def snap_save(self, path='./test.png'):
        ret, frame = self.snap()
        if ret:
            cv.imwrite(path, frame)
        return ret

    def absMove(self, pan, tilt, zoom=0):
        if self.inited:
            self.ptz = self.cam.create_ptz_service()
            request = self.ptz.create_type('AbsoluteMove')
            request.ProfileToken = self.profile.token
            request.Position = {'PanTilt': {'x': pan / 180, 'y': tilt / 180}, 'Zoom': zoom}
            self.ptz.AbsoluteMove(request)

    def relativeMove(self, pan, tilt, zoom=0):
        if self.inited:
            self.ptz = self.cam.create_ptz_service()
            request = self.ptz.create_type('RelativeMove')
            request.ProfileToken = self.profile.token

            request.Translation = {'PanTilt': {'x': pan / 180, 'y': tilt / 180}, 'Zoom': zoom}
            self.ptz.RelativeMove(request)

    def continue_move_image(self, speed=0.5):
        if self.inited:
            request = self.imaging.create_type('Move')
            request.VideoSourceToken = self.profile.VideoSourceConfiguration.SourceToken
            request.Focus = {'Continuous': {'Speed': speed}}
            self.imaging.Move(request)



if __name__ == '__main__':
    cam = HKPTZCamera()
    cam.init()
    cam.absMove(90, 90)
