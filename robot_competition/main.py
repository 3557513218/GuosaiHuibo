import time

from car import SongLingCar,HbCar
from fr_robot import FrRobot
from carry import Carry
from utils import *
from config import *
from enum import Enum,unique
from copy import deepcopy


@unique
class CarryState(Enum):
    Error=0
    CarryToImgPoint=1
    TakePicture=2
    ImageRec=3
    CarryPick=4
    CarryPlace=5
    CarryToHome=6

class Arm():
    def __init__(self,ip,port):
        self._arm=FrRobot(ip,port)
        self._arm.startProcess()

    def moveJ(self,pose):
        flag, result=self._arm.moveJ(*pose)
        if flag:
            print("机械臂轨迹规划成功")
        else:
            print("机械臂目标点位无法到达")
            raise ArmError("机械臂目标点位无法到达")

    def cameraRecongnize(self,armCurrentPose,armPickPose,cameraExtrinsic,markerLength,cameraMatrix,distCoeffs):
        cameraFlag, cameraResult = HbCar.realsenseCamera(1)
        if not cameraFlag:
            raise ImageRecError("图像拍照错误")
        temList = cameraResult.split("/")
        imagePath = os.path.join(imgSaveDir, temList[-1])
        imgFlag = copy_pictures(agvIP, cameraResult, imagePath)
        if not imgFlag:
            raise ImageRecError("拷贝机械臂相机失败")
        endToRobotPoseRt, endToRobotPoseR, endToRobotPoseT = tcpToRobot(*armCurrentPose)
        imgRecFlag,imgRecResult=getArucoPose(imagePath,markerLength,cameraMatrix,distCoeffs)
        if not imgRecFlag:
            raise ImageRecError("相机识别错误")
        ids, rvec, tvec = imgRecResult
        tvec *= 1000
        targetToCameraPoseRt, targetToCameraPoseR, targetToCameraPoseT = targetToCamera(tvec[0, 0, 0], tvec[0, 0, 1],
                                                                                        tvec[0, 0, 2], rvec[0, 0, 0],
                                                                                        rvec[0, 0, 1], rvec[0, 0, 2])
        # R_x180 = RPY2R_robot(180, 0, 0)
        # t_x180 = np.array([0, 0, 0])
        # Rt_x180 = R_T2RT(R_x180, t_x180)
        # pose = endToRobotPoseRt @ cameraExtrinsic @ targetToCameraPoseRt @ Rt_x180
        pose = endToRobotPoseRt @ cameraExtrinsic @ targetToCameraPoseRt
        targetR, targetT = RT2R_T(pose)
        targeteuler = rot2euler(targetR)
        targetT[2] = armPickPose[2]
        targeteuler[0]=armPickPose[3]
        targeteuler[1] = armPickPose[4]
        return [*targetT,*targeteuler]

    def armMoveByCamera(self,imagePoint,targetPoint,temPoints=None):
        imgRecResult=self.cameraRecongnize(imagePoint,targetPoint,realsenseCameraExtrinsic,markerLength,realsenseCameraMatrix,realsenseDistCoeffs)
        movePoints=[]
        if temPoints is not None:
            for temPoint in temPoints:
                movePoints.append(temPoint)
        movePointEnd=deepcopy(imgRecResult)
        movePointEnd[2]+=50
        movePoints.append(movePointEnd)
        movePoints.append(imgRecResult)
        for movePoint in movePoints:
            self.moveJ(movePoint)
            while True:
                time.sleep(1)
                if self._arm.moveFlag == 1:
                    break

    def armContinuityMove(self,points):
        for point in points:
            self.moveJ(point)
            while True:
                time.sleep(1)
                if self._arm.moveFlag == 1:
                    break

    def griberOpen(self):
        flag, result=self._arm.setDO(1, 0)
        if not flag:
            raise ArmError("机械臂IO设置错误")
        time.sleep(2)

    def griberClose(self):
        flag, result=self._arm.setDO(1, 1)
        if not flag:
            raise ArmError("机械臂IO设置错误")
        time.sleep(2)

    def __del__(self):
        self._arm.stopProcess()

class WorkProcess():
    def __init__(self):
        self.running=True
        self.robot=Arm("192.168.8.100",8080)
        self.carry=Carry("192.168.8.50")
        self.carry.startProcess()

    def acmCarMoveToPose(self,pose):
        flag, ret = SongLingCar.moveToPose(pose)
        if flag and (ret["result"] == 5):
            print(f"导航成功")
        else:
            if not flag:
                raise CarError("阿克曼车导航网络请求错误")
            else:
                raise CarError(f"导航失败,导航返回值{ret['result']}")

    def waitAcmMoveDone(self):
        while True:
            print("智能接驳车导航中.....")
            flag, ret = SongLingCar.getNavigationState()
            if flag and (ret["result"] == "sucess"):
                break

    def agvMoveToPose(self,pose):
        flag, ret = HbCar.moveToPose(pose)
        if flag and (ret["error_code"] == 0):
            print(f"导航成功")
        else:
            if not flag:
                raise AgvError("AGV导航网络请求错误")
            else:
                raise AgvError(f"AGV导航失败,导航返回值{ret['error_code']}")

    def waitAgvMoveDone(self):
        while True:
            print("智能接驳车导航中.....")
            flag, ret = HbCar.getNavigationState()
            if flag and (ret["result"] == "success"):
                break

    def agvManualMoveDist(self):
        HbCar.manualMove(0.2,0)
        time.sleep(3)
        HbCar.manualMove(0, 0)


    def carryMove(self,carry, point):
        resp = False
        try:
            carry.absMove(point)
            print(f"桥吊运动成功，目标点:{point}")
            resp = True
        except:
            print("桥吊运动失败")
        if resp:
            time.sleep(5)
            while self.running:
                print("桥吊运动中...")
                try:
                    if carry.getMoveState() == 1:
                        print("桥吊运动完成")
                        break
                except:
                    print("获取桥吊数据失败")
                time.sleep(0.1)
        return resp

    def transport(self,carry,pickImgPoint,pickRecRefer,pickReferPoint,placeImgPoint,placeRecRefer,placeReferPoint,markerLength, cameraMatrix, distCoeffs):
        self.imgPath = os.path.join(imgDir, get_picture_name())
        self.carryState=CarryState.CarryToImgPoint.value
        self.imgPoint=pickImgPoint
        self.temPoint=None
        self.pickDoneFlag=False
        print("桥吊开始搬运")
        while self.running:
            if self.carryState==CarryState.Error.value:
                print("桥吊搬运错误")
                raise CarryError(f"桥吊搬运错误")
            elif self.carryState==CarryState.CarryToImgPoint.value:
                if not self.carryMove(carry, self.imgPoint):
                    self.carryState = CarryState.Error.value
                else:
                    self.carryState=CarryState.TakePicture.value
            elif self.carryState == CarryState.TakePicture.value:
                self.imgPath = os.path.join(imgDir, get_picture_name())
                if getCameraImgDH(self.imgPath):
                    self.carryState=CarryState.ImageRec.value
                else:
                    print("桥吊相机拍照失败")
                    self.carryState = CarryState.Error.value
            elif self.carryState == CarryState.ImageRec.value:
                flag, result = getArucoPose(self.imgPath, markerLength, cameraMatrix, distCoeffs)
                if flag:
                    ids, rvec, tvec=result
                    if self.pickDoneFlag:
                        poseTem = placeReferPoint.copy()
                        poseTem[0] -= (tvec[0, 0, 0] - placeRecRefer[0]) * 1000
                        poseTem[1] += (tvec[0, 0, 1] - placeRecRefer[1]) * 1000
                    else:
                        poseTem = pickReferPoint.copy()
                        poseTem[0] -= (tvec[0, 0, 0] - pickRecRefer[0]) * 1000
                        poseTem[1] += (tvec[0, 0, 1] - pickRecRefer[1]) * 1000
                    poseTem[2] += 100
                    self.temPoint=poseTem
                    if self.pickDoneFlag:
                        self.carryState=CarryState.CarryPlace.value
                    else:
                        self.carryState = CarryState.CarryPick.value

                else:
                    print("桥吊相机图像识别失败")
                    self.carryState = CarryState.Error.value
            elif self.carryState == CarryState.CarryPick.value:
                temPoint=self.temPoint.copy()
                targetPoint=self.temPoint.copy()
                targetPoint[2]-=100
                if (self.carryMove(carry, temPoint)) and (self.carryMove(carry, targetPoint)):
                    carry.magnetic(1)
                    self.pickDoneFlag=True
                    self.imgPoint=placeImgPoint
                    self.carryState=CarryState.CarryToImgPoint.value
                else:
                    self.carryState = CarryState.Error.value

            elif self.carryState == CarryState.CarryPlace.value:
                temPoint=self.temPoint.copy()
                targetPoint=self.temPoint.copy()
                targetPoint[2]-=100
                if (self.carryMove(carry, temPoint)) and (self.carryMove(carry, targetPoint)):
                    carry.magnetic(0)
                    self.carryState=CarryState.CarryToHome.value
                else:
                    self.carryState = CarryState.Error.value
            elif self.carryState==CarryState.CarryToHome.value:
                if (self.carryMove(carry, self.temPoint)) and (self.carryMove(carry, (0,0,0))):
                    print("桥吊搬运完成")
                    return True
                else:
                    self.carryState = CarryState.Error.value

    def pick(self,agvPointAtCar_,pickPoints01,pickPoints02,pickPoints03,pickPoints04):
        self.agvMoveToPose(agvPointAtCar_)
        self.waitAgvMoveDone()
        self.robot.armContinuityMove(pickPoints01)
        self.robot.armMoveByCamera(armPickImagePose,armPickPoseCar,armPickTemPose)
        self.robot.griberClose()
        self.robot.armContinuityMove(pickPoints02)
        self.agvManualMoveDist()
        self.robot.armContinuityMove(pickPoints03)
        self.robot.griberOpen()
        self.robot.armContinuityMove(pickPoints04)


    def place(self,agvPointAtStorageArea_,placePoint01,placePoint02,placePoint03,placePoint04):
        self.agvMoveToPose(agvPointAtStorageArea_)
        self.waitAgvMoveDone()
        self.robot.armContinuityMove(placePoint01)
        self.robot.griberClose()
        self.robot.armContinuityMove(placePoint02)
        self.robot.armMoveByCamera(armPlaceImagePose,armPlacePoseStorage,armPlaceTemPose)
        self.robot.griberOpen()
        self.robot.armContinuityMove(placePoint03)
        self.agvManualMoveDist()
        self.robot.armContinuityMove(placePoint04)


    def process(self,carryCnt,storageCnt):
        carryPickImgPoints=[]
        carryPickRecRefers=[]
        carryPickReferPoints=[]
        agvPointAtStorageAreas=[]
        carryPickImgPoints.append(carryPickImgPoint01)
        carryPickImgPoints.append(carryPickImgPoint02)
        carryPickImgPoints.append(carryPickImgPoint03)
        carryPickRecRefers.append(carryPickRecRefer01)
        carryPickRecRefers.append(carryPickRecRefer02)
        carryPickRecRefers.append(carryPickRecRefer03)
        carryPickReferPoints.append(carryPickReferPoint01)
        carryPickReferPoints.append(carryPickReferPoint02)
        carryPickReferPoints.append(carryPickReferPoint03)
        agvPointAtStorageAreas.append(agvPointAtStorageArea01)
        agvPointAtStorageAreas.append(agvPointAtStorageArea02)
        agvPointAtStorageAreas.append(agvPointAtStorageArea03)

        self.acmCarMoveToPose(carPointAtCarry)
        self.waitAcmMoveDone()
        self.transport(self.carry,carryPickImgPoints[carryCnt],carryPickRecRefers[carryCnt],carryPickReferPoints[carryCnt],carryPlaceImgPoint,carryPlaceRecRefer,carryPlaceReferPoint,markerLength, dhCameraMatrix, dhDistCoeffs)
        self.acmCarMoveToPose(carPointAtStorageArea)
        self.waitAcmMoveDone()
        self.pick(agvPointAtCar,pickPoints01,pickPoints02,pickPoints03,pickPoints04)
        self.place(agvPointAtStorageAreas[storageCnt],placePoint01,placePoint02,placePoint03,placePoint04)

if __name__ == '__main__':
    WorkProcess().process()
    # placeTest()











