import cv2
from sympy.strategies.core import switch

from ui.ui_mainwindow import Ui_MainWindow
from camera_client import CameraClient
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

import os
import datetime

class MainWindow(QMainWindow):
    __deg1 = 0
    __deg2 = 0
    __camera = None
    __image_cnt = 0

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()  # UI类的实例化
        self.ui.setupUi(self)
        #控件默认值
        self.ui.btnCloseCamera.setDisabled(True)
        self.ui.comboBoxType.setCurrentIndex(2)
        #信号连接
        self.ui.btnConnectCamera.clicked.connect(self.slotBtnConnectCamera)
        self.ui.btnCloseCamera.clicked.connect(self.slotCLoseCamera)
        self.ui.currDeg1.valueChanged.connect(self.slotDeg1Changed)
        self.ui.currDeg2.valueChanged.connect(self.slotDeg2Changed)
        self.ui.btnDeg1Up.clicked.connect(self.slotDeg1UpClicked)
        self.ui.btnDeg1Down.clicked.connect(self.slotDeg1DownClicked)
        self.ui.btnDeg2Up.clicked.connect(self.slotDeg2UpClicked)
        self.ui.btnDeg2Down.clicked.connect(self.slotDeg2DownClicked)

        self.ui.btnSetSavePath.clicked.connect(self.slotSetSavePath)
        self.ui.btnSaveImage.clicked.connect(self.slotSaveImage)
        #相机初始化
        self.__camera = CameraClient()
        self.__camera.signal_int.connect(self.slot_connect)
        self.__camera.signal_img.connect(self.slotImageUpdate)

    def slot_connect(self, state):
        self.ui.labelConnectState.setText(state)
        if self.__camera.is_connect:
            #连接成功
            self.ui.btnConnectCamera.setDisabled(True)
            self.ui.btnCloseCamera.setDisabled(False)
            QMessageBox.information(self, "信息", "已连接相机", QMessageBox.Ok)
        else:
            self.ui.btnConnectCamera.setDisabled(False)
            self.ui.btnCloseCamera.setDisabled(True)

    #打开相机
    def slotBtnConnectCamera(self):
        self.__camera.start()
        self.__image_cnt = 0
        self.ui.labelCurrImgNum.setText("已采集数量:0")

    #关闭相机
    def slotCLoseCamera(self):
        if self.__camera.isRunning():
            self.__camera.stop()

    #图像更新
    def slotImageUpdate(self):
        #拿到图像
        frame = self.__camera.image
        # frame = cv2.resize(frame, (1920,1080))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #转换pixmap
        height, width = frame.shape[:2]
        pixmap = QImage(frame, width, height, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(pixmap)
        #缩放比例 适配窗口大小显示
        ratio = max(width / self.ui.labelImage.width(), height / self.ui.labelImage.height())
        pixmap.setDevicePixelRatio(ratio)
        self.ui.labelImage.setAlignment(Qt.AlignCenter)
        self.ui.labelImage.setPixmap(pixmap)

    #保存图片路径按键
    def slotSetSavePath(self):
        folder_path = QFileDialog.getExistingDirectory(window, "选择保存文件夹")
        if folder_path:
            self.ui.lineEditSavePath.setText(folder_path)
    #保存图片
    def slotSaveImage(self):
        #未连接相机 弹窗警告
        if not self.__camera.is_connect:
            QMessageBox.information(self, "警告", "请连接相机", QMessageBox.Ok)
            return
        #检查保存路径是否存在
        save_path = self.ui.lineEditSavePath.text()
        if not os.path.exists(save_path):
            QMessageBox.information(self, "警告", "请设置图片保存路径", QMessageBox.Ok)
            return
        #保存图片
        frame = self.__camera.image
        file_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f") + '.png'
        file_path = os.path.join(save_path, file_name)
        #处理保存分辨率
        idx = self.ui.comboBoxType.currentIndex()
        txt = self.ui.comboBoxType.currentText()
        img = None
        if idx == 1:
            #1920x1080
            img = cv2.resize(frame, (1920,1080))
        elif idx == 2:
            img = cv2.resize(frame, (640, 480))
        elif idx == 3:
            img = cv2.resize(frame, (320, 240))
        else:
            img = frame
        if cv2.imwrite(file_path, img) != -1:
            #保存成功
            self.__image_cnt += 1
            str_txt = "已采集数量:" + str(self.__image_cnt)
            self.ui.labelCurrImgNum.setText(str_txt)

    #云台控制
    def slotDeg1Changed(self, val):
        self.__deg1 = val
        self.__camera.move(self.__deg1, self.__deg2)

    def slotDeg2Changed(self, val):
        self.__deg2 = val
        self.__camera.move(self.__deg1, self.__deg2)

    def slotDeg1UpClicked(self):
        self.__deg1 += 1
        if self.__deg1 > 180:
            self.__deg1 = 180
        self.ui.currDeg1.setValue(self.__deg1)

    def slotDeg1DownClicked(self):
        self.__deg1 -= 1
        if self.__deg1 < -180:
            self.__deg1 = -180
        self.ui.currDeg1.setValue(self.__deg1)

    def slotDeg2UpClicked(self):
        self.__deg2 += 1
        if self.__deg2 > 180:
            self.__deg2 = 180
        self.ui.currDeg2.setValue(self.__deg2)

    def slotDeg2DownClicked(self):
        self.__deg2 -= 1
        if self.__deg2 < -180:
            self.__deg2 = -180
        self.ui.currDeg2.setValue(self.__deg2)

if __name__ == '__main__':
    app = QApplication([])  # 启动一个应用
    window = MainWindow()  # 实例化主窗口
    window.show()  # 展示主窗口
    app.exec()  # 避免程序执行到这一行后直接退出