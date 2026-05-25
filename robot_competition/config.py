import numpy as np
#--------------------------------------------阿克曼车------------------------------------------
carPointAtCarry=[0,0,0] #吊桥下
carPointAtStorageArea=[1.5,-2.5,0]  #开到对接点
#---------------------------------------------agv---------------------------------------------
agvIP="192.168.8.21"
imgSaveDir="./images"   #机械臂拍照图片保存路径
agvPointAtCar=[2.23138,0.71920,-2.89080]   #新能源车对接点
agvPointAtStorageArea01=[-1.10665,-5.02537,-0.04826]    #安全处置柜点位1
agvPointAtStorageArea02=[-1.10665,-5.02537,-0.04826]    #安全处置柜点位2
agvPointAtStorageArea03=[-1.10665,-5.02537,-0.04826]    #安全处置柜点位3

#---------------------------------------------机械臂-------------------------------------------
armHomePose=[174.388,-98.526,97.902,-91.606,-87.512,1.349]   #home点
armPickImagePose=[-5.916,-78.597,86.06,-87.454,-0.575]    #抓取拍照点
armPickPoseCar=[-577.371,-85.41,58,179.173,0.516,93.171]    #抓取参考位置
armPickTemPose=None
armPickTem01=[-8.168,-81.873,57.47,-64.738,-87.468,-0.815]#机械臂抓取盒子后放置到车上过渡点1
armPickTem02=[-179.832,-99.244,102.515,-94.013,-91.971,-0.697]#机械臂抓取盒子后放置到车上过渡点2
armPickPoseAgv=[-179.714,-80.71,115.874,-125.471,-91.967,-0.722]#机械臂抓取盒子后放置到车上过渡点3

armPlaceImagePose=[-435.582,-74.755,330,179.277,0,92.062]#放置拍照点
armPlacePoseStorage=[-573.979,-81.217,110,-179.577,0.185,170.364]#放置参考位置
armPlaceTemPose=None
armPlaceTem01=[77.683,-397.076,412.067,-179.574,0.147,-177.123]#机械臂抓取盒子后放置到货柜过渡点1
armPLaceTem02=[77.683,-397.076,412.067,-179.574,0.147,-177.123]#机械臂抓取盒子后放置到货柜过渡点2

pickPoints01=[armPickImagePose,armPickPoseCar]  #到达拍照点
pickPoints02=[armPickImagePose] #抓取盒子后机械臂电位
pickPoints03=[armPickTem01,armPickTem02,armPickPoseAgv] #将盒子放到AGV上机械臂电位
pickPoints04=[armPickTem02,armPickTem01,armHomePose]    #将盒子放到AGV后机械臂电位
placePoint01=[armPickTem01,armPickTem02,armPickPoseAgv] #从AGV上取盒子机械臂电位
placePoint02=[armPickTem02,armPickTem01,armPlaceTem01,armPLaceTem02]    #从AGV上取盒子后机械臂电位
placePoint03=[armPlaceImagePose,armPlacePoseStorage]    #将盒子放到柜子上机械臂电位
placePoint04=[armPlaceImagePose]    #将盒子放到柜子后机械臂电位
#-------------------------------------------桥吊----------------------------------------------
carryPickImgPoint01=[10,-789,0] #抓取拍照位置1
carryPickRecRefer01=[0.22850805, 0.11855817, 0.09073573] #抓取拍照参考值1
carryPickReferPoint01=[-3,-1001,-178]   #抓取位置参考值1
carryPickImgPoint02=[0,0,0] #抓取拍照位置2
carryPickRecRefer02=[0,0,0] #抓取拍照参考值2
carryPickReferPoint02=[0,0,0]       #抓取位置参考值3
carryPickImgPoint03=[0,0,0] #抓取拍照位置3
carryPickRecRefer03=[0,0,0] #抓取拍照参考值2
carryPickReferPoint03=[0,0,0]   #抓取位置参考值3

carryPlaceImgPoint=[30,371,0]  #放置拍照位置
carryPlaceRecRefer=[0.4423756 , 0.1870152 , 0.16344509]  #放置拍照参考值
carryPlaceReferPoint=[30,50,-314]    #放置位置参考值


markerLength=0.07   #aruco码长度
imgDir="./images" #桥吊拍照图片路径
#----------------------------------------机械臂相机-------------------------------------------
#机械臂相机内参
realsenseCameraMatrix=np.matrix([[607.9772338867188, 0.0, 322.93621826171875],
            [0.0, 607.4258422851562, 240.17523193359375],
            [0,0,1]],dtype=np.float64)
#机械臂相机畸变系数
realsenseDistCoeffs=np.array([0.0, 0.0, 0.0, 0.0])
#机械臂相机外参
realsenseCameraExtrinsic=np.array([[ 0.99789025, -0.04967131, -0.04180687, -20.43297],
 [ 0.04850729,  0.99841865 ,-0.02841197, -117.0],
 [ 0.04315202 , 0.02632409 , 0.99872166, -19.65488],
 [ 0.  ,        0.    ,      0.     ,     1.        ]])
#----------------------------------------桥吊相机--------------------------------------------
#桥吊相机内参
dhCameraMatrix=np.matrix([[607.9772338867188, 0.0, 322.93621826171875],
            [0.0, 607.4258422851562, 240.17523193359375],
            [0,0,1]],dtype=np.float64)
#桥吊相机畸变系数
dhDistCoeffs=np.array([0.0, 0.0, 0.0, 0.0])
