import sys
import time
import cv2
import os
import numpy as np
import cv2.aruco as aruco
from func_timeout import    func_set_timeout
import paramiko
import functools
import logging
import traceback
from scipy.spatial.transform import Rotation as R
import math

logger  = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("./log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class ArmError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class ImageRecError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class AgvError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class CarError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class CarryError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

def try_except(fn):
    @functools.wraps(fn)
    def inner(*args,**kwargs):
        flag = False
        result = None
        try:
            result= fn(*args,**kwargs)
            flag=True
        except Exception as e:
            print(e)
            exc_type, exc_instance, exc_traceback = sys.exc_info()
            formatted_traceback = ''.join(traceback.format_tb(exc_traceback))
            message = '\n{0}\n{1}:\n{2}'.format(
                formatted_traceback,
                exc_type.__name__,
                exc_instance
            )
            logger.warning(exc_type(message))
        return flag,result
    return inner

@try_except
def copy_pictures(host, remotepath, localpath):
    transport = paramiko.Transport((host, 22))
    transport.connect(username="kilox", password="123456")
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.get(remotepath, localpath)
    transport.close()

def get_picture_name():
    return time.strftime("%Y%m%d%H%M%S")+".jpg"

def getArucoPose1(frame,markerLength,cameraMatrix,distCoeffs,show=False,path="./aruco.jpg"):
    flag=False
    result=None
    if isinstance(frame,str):
        frame = cv2.imread(frame)
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, frame.shape[:2], 0, frame.shape[:2])
    img_undistorted = cv2.undistort(frame, cameraMatrix, distCoeffs, None, newcameramtx)
    gray = cv2.cvtColor(img_undistorted, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_1000)
    parameters = aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    if ids is not None:
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, markerLength, cameraMatrix, distCoeffs)
        for i in range(rvec.shape[0]):
            aruco.drawAxis(frame, cameraMatrix, distCoeffs, rvec[i, :, :], tvec[i, :, :], 0.03)
            aruco.drawDetectedMarkers(frame, corners)
        cv2.putText(frame, "Id: " + str(ids), (0, 64), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imwrite(path,frame)
        if show:
            cv2.imshow("frame", frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        flag=True
        result=ids,rvec, tvec
    return flag,result

#
def getArucoPose2(frame,markerLength,cameraMatrix,distCoeffs,show=False,path="./aruco.jpg"):
    flag = False
    result = None
    if isinstance(frame, str):
        frame = cv2.imread(frame)
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, frame.shape[:2], 0, frame.shape[:2])
    img_undistorted = cv2.undistort(frame, cameraMatrix, distCoeffs, None, newcameramtx)
    gray = cv2.cvtColor(img_undistorted, cv2.COLOR_BGR2GRAY)
    parameters = aruco.DetectorParameters()
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_1000)
    detector = aruco.ArucoDetector(aruco_dict, parameters)
    corners, ids, rejectedImgPoints = detector.detectMarkers(gray)
    if ids is not None:
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, markerLength, cameraMatrix, distCoeffs)
        for i in range(rvec.shape[0]):
            cv2.drawFrameAxes(frame, cameraMatrix, distCoeffs, rvec[i, :, :], tvec[i, :, :], 0.03)
            aruco.drawDetectedMarkers(frame, corners)
        cv2.putText(frame, "Id: " + str(ids), (0, 64), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imwrite(path, frame)
        if show:
            cv2.imshow("frame", frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        flag = True
        result = ids, rvec, tvec
    return flag, result

def getArucoPose3(frame,markerLength,cameraMatrix,distCoeffs,show=False,path="./aruco.jpg"):
    flag = False
    result = None
    if isinstance(frame, str):
        frame = cv2.imread(frame)
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, frame.shape[:2], 0, frame.shape[:2])
    img_undistorted = cv2.undistort(frame, cameraMatrix, distCoeffs, None, newcameramtx)
    gray = cv2.cvtColor(img_undistorted, cv2.COLOR_BGR2GRAY)
    gray=255-cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,55,0)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_1000)
    parameters = aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    if ids is not None:
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, markerLength, cameraMatrix, distCoeffs)
        for i in range(rvec.shape[0]):
            aruco.drawAxis(frame, cameraMatrix, distCoeffs, rvec[i, :, :], tvec[i, :, :], 0.03)
            aruco.drawDetectedMarkers(frame, corners)
        cv2.putText(frame, "Id: " + str(ids), (0, 64), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imwrite(path,frame)
        if show:
            for i in range(rvec.shape[0]):
                aruco.drawAxis(frame, cameraMatrix, distCoeffs, rvec[i, :, :], tvec[i, :, :], 0.03)
                aruco.drawDetectedMarkers(frame, corners)
            cv2.putText(frame, "Id: " + str(ids), (0, 64), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow("frame", frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        flag = True
        result = ids, rvec, tvec
    return flag, result

def getArucoPose4(frame,markerLength,cameraMatrix,distCoeffs,show=False,path="./aruco.jpg"):
    flag = False
    result = None
    if isinstance(frame, str):
        frame = cv2.imread(frame)
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, frame.shape[:2], 0, frame.shape[:2])
    img_undistorted = cv2.undistort(frame, cameraMatrix, distCoeffs, None, newcameramtx)
    gray = cv2.cvtColor(img_undistorted, cv2.COLOR_BGR2GRAY)
    gray = 255 - cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 101, 0)
    parameters = aruco.DetectorParameters()
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_1000)
    detector = aruco.ArucoDetector(aruco_dict, parameters)
    corners, ids, rejectedImgPoints = detector.detectMarkers(gray)
    if ids is not None:
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, markerLength, cameraMatrix, distCoeffs)
        for i in range(rvec.shape[0]):
            cv2.drawFrameAxes(frame, cameraMatrix, distCoeffs, rvec[i, :, :], tvec[i, :, :], 0.03)
            aruco.drawDetectedMarkers(frame, corners)
        cv2.putText(frame, "Id: " + str(ids), (0, 64), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imwrite(path, frame)
        if show:
            cv2.imshow("frame", frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        flag = True
        result = ids, rvec, tvec
    return flag, result

def getArucoPose(frame,markerLength,cameraMatrix,distCoeffs,show=False,path="./aruco.jpg"):
    version = float(cv2.__version__[:3])
    if version>=4.6:
        flag,result=getArucoPose2(frame,markerLength,cameraMatrix,distCoeffs,show,path)
        if flag:
            return flag,result
        return getArucoPose4(frame,markerLength,cameraMatrix,distCoeffs,show,path)
    else:
        flag, result = getArucoPose1(frame, markerLength, cameraMatrix, distCoeffs, show,path)
        if flag:
            return flag, result
        return getArucoPose3(frame, markerLength, cameraMatrix, distCoeffs, show,path)




class Rec():
    def __init__(self,model,labels,conf_thres=0.85,iou_thres=0.5):
        self.model=model
        self.conf_thres=conf_thres
        self.iou_thres=iou_thres
        self.labels=labels
        self.flag=self.model.split(".")
        if self.flag[-1]=="onnx":
            from yolo import Yolov8
            self.model=Yolov8(self.model,self.conf_thres, self.iou_thres,self.labels)
        elif self.flag[-1] == "pt":
            from ultralytics import YOLO
            self.model = YOLO(model=model)

    def detect(self,path,show=False):
        if self.flag[-1] == "onnx":
            return self.model.main(path,show)
        elif self.flag[-1] == "pt":
            img = cv2.imread(path)
            #img = cv2.flip(img, 1)
            results = self.model.predict(source=img, conf=self.conf_thres, iou=self.iou_thres, device="cpu")
            names = results[0].names
            ret = []
            cls = results[0].boxes.cls.numpy()
            boxes = results[0].boxes.boxes.numpy()
            boxs = {}
            for box in boxes:
                tem = box[:4].tolist()
                center = [(tem[0] + tem[2]) / 2, (tem[1] + tem[3]) / 2]
                boxs[int(box[-1])] = center
            for c in cls:
                ret.append({"flag": self.labels[int(c)], "center": boxs[int(c)]})
            if show:
                frame = results[0].plot()
                cv2.imshow("img", frame)
                cv2.waitKey(10)
            return ret

def rotvector2rot(rotvector):
    '''
    旋转向量转旋转矩阵
    :param rotvector:
    :return:旋转矩阵
    '''
    return cv2.Rodrigues(rotvector)[0]

def quaternion2euler(quaternion,type="xyz",degrees=True):
    '''
    四元数转欧拉角
    :param quaternion: 四元数
    :param type:欧拉角类型
    :param degrees:角度?弧度
    :return: 欧拉角(默认degrees)
    '''
    r = R.from_quat(quaternion)
    return r.as_euler(type, degrees)

def euler2quaternion(euler,type="xyz",degrees=True):
    '''
    欧拉角转四元数
    :param euler:欧拉角
    :param type:欧拉角类型
    :param degrees:角度?弧度
    :return:四元数
    '''
    r = R.from_euler(type, euler,degrees)
    return r.as_quat()

def euler2rot(euler,type="xyz",degrees=True):
    '''
    欧拉角转旋转矩阵
    :param euler:欧拉角
    :param type:欧拉角类型
    :param degrees:角度?弧度
    :return:旋转矩阵
    '''
    r = R.from_euler(type, euler, degrees)
    return r.as_matrix()

def isRotationMatrix(R):
    '''
    是否为旋转矩阵
    :param R: 矩阵
    :return:
    '''
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype=R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6

def quaternion2rot(quaternion):
    '''
    四元数转旋转矩阵
    :param quaternion:四元数
    :return:旋转矩阵
    '''
    r = R.from_quat(quaternion)
    return r.as_matrix()


def rot2euler(R):
    assert (isRotationMatrix(R))

    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2]) * 180 / np.pi
        y = math.atan2(-R[2, 0], sy) * 180 / np.pi
        z = math.atan2(R[1, 0], R[0, 0]) * 180 / np.pi
    else:
        x = math.atan2(-R[1, 2], R[1, 1]) * 180 / np.pi
        y = math.atan2(-R[2, 0], sy) * 180 / np.pi
        z = 0

    return np.array([x, y, z])

def tcpToRobot(x,y,z,rx,ry,rz):
    R=euler2rot((rx,ry,rz),type="xyz",degrees=True)
    t = np.array([[x], [y], [z]])
    Rt=np.column_stack([R, t])
    Rt=np.row_stack((Rt, np.array([0,0,0,1])))
    return Rt,R,t

def targetToCamera(x,y,z,rx,ry,rz):
    rotvector = np.array([[rx,ry,rz]])
    R=rotvector2rot(rotvector)
    t = np.array([[x], [y], [z]])
    Rt = np.column_stack([R, t])
    Rt = np.row_stack((Rt, np.array([0, 0, 0, 1])))
    return Rt,R,t

def R_T2RT(R,t):
    Rt = np.column_stack([R, t])
    Rt = np.row_stack((Rt, np.array([0, 0, 0, 1])))
    return Rt

def RT2R_T(Rt):
    R=Rt[0:3,0:3]
    t=np.array([Rt[0,3],Rt[1,3],Rt[2,3]])
    return R,t


def RPY2R_robot(x, y, z):
    thetaX = x / 180 * math.pi
    thetaY = y / 180 * math.pi
    thetaZ = z / 180 * math.pi
    Rx = np.array([[1, 0, 0], [0, math.cos(thetaX), -math.sin(thetaX)], [0, math.sin(thetaX), math.cos(thetaX)]])
    Ry = np.array([[math.cos(thetaY), 0, math.sin(thetaY)], [0, 1, 0], [-math.sin(thetaY), 0, math.cos(thetaY)]])
    Rz = np.array([[math.cos(thetaZ), -math.sin(thetaZ), 0], [math.sin(thetaZ), math.cos(thetaZ), 0], [0, 0, 1]])
    R = Rz@Ry@Rx
    # R = Rx @ Ry @ Rz
    return R

@try_except
@func_set_timeout(5)
def getCameraImgDH(savePath):
    isSuccess = False
    cap = cv2.VideoCapture(
        'rtsp://192.168.8.52:554/user=admin&password=&channel=1&stream=0.sdp?')
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(savePath, frame)
            isSuccess=True
        else:
            print("图像获取失败")
        cap.release()
    return isSuccess



if __name__ == '__main__':
    from config import *
    imagePath = "/home/hb/人工智能训练师2024/服务机器人2024/images/11.jpg"
    getCameraImgDH(imagePath)
    res = getArucoPose(imagePath,markerLength,dhCameraMatrix,dhDistCoeffs)
    print(res)


