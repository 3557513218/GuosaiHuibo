import sys
import os
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QPixmap
from ui.ui_main import Ui_MainWindow

# 添加共享库路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../lib'))

from utils import genJson
from meter_reading import showmaV
from config import Config
from train_engine import trainyolo
from ultralytics import YOLO
import shutil

os.environ['WANDB_DISABLED'] = 'true'


class TrainingThread(QThread):
    # 定义信号，用于更新训练日志
    updateLogSignal = Signal(str)

    def __init__(self, learning_rate, epochs, batch_size, name, class_names,app):
        super().__init__()
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.batch_size = batch_size
        self.name = name
        self.class_names = class_names
        self.app = app
    def run(self):
        try:
            genJson(Config.dataset_path, self.class_names)
            self.updateLogSignal.emit('数据加载完成，开始训练...')
            trainyolo(self.learning_rate, self.epochs, self.batch_size, self.name,self.app)
            pixmap = QPixmap('./runs/detect/{}/results.png'.format(Config.name))  # 替换为你的图片路径
            scaled_pixmap = pixmap.scaled(self.app.showimg_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.app.showimg_label.setPixmap(scaled_pixmap)
            self.updateLogSignal.emit("训练完成！")
        except Exception as e:
            self.updateLogSignal.emit(f"训练失败: {e}")


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.class_name = []
        self.testImgpath = ''
        self.model = None
        # 数据导入部分信号
        self.importData_btn.clicked.connect(self.importData)
        self.importCls_btn.clicked.connect(self.importCls)

        # 训练部分信号
        self.startTrain_btn.clicked.connect(self.startTrain)
        #测试部分信号
        self.testImgImport_btn.clicked.connect(self.importTestimg)
        self.startTest_btn.clicked.connect(self.startTest)
        #保存模型部分信号
        self.saveModel_btn.clicked.connect(self.saveModel)

    # ------------------------------------------------------数据导入部分----------------------------------------------------
    def importData(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择数据集文件夹")
        if folder_path:
            Config.dataset_path = folder_path  # 更新配置对象
            QMessageBox.information(self, "信息", f"数据集文件夹导入成功：{Config.dataset_path}")

    def importCls(self):
        classtxt, _ = QFileDialog.getOpenFileName(self, "选择类别文件", "", "文本文件 (*.txt)")
        if classtxt:  # 确保文件选择不为空
            try:
                with open(classtxt, 'r', encoding='utf-8') as file:
                    self.class_name = [line.strip() for line in file.readlines()]
                # 更新文本框内容
                self.clsShow_text.setPlainText('\n'.join(self.class_name))
            except Exception as e:
                QMessageBox.critical(self, "错误", f"读取文件时发生错误: {e}")

    # -------------------------------------------------训练部分-------------------------------------------------
    def startTrain(self):
        try:
            Config.learning_rate = float(self.lr_text.text())
            Config.epochs = int(self.epoch_text.text())
            Config.batch_size = int(self.bs_text.text())
            Config.name = self.prjName_text.text()
            if os.path.isdir('./runs/detect/{}'.format(Config.name)):
                QMessageBox.critical(self, '警告', '已经存在该项目')
            else:
                # 创建训练线程
                self.train_thread = TrainingThread(Config.learning_rate, Config.epochs, Config.batch_size, Config.name, self.class_name,self)
                self.train_thread.updateLogSignal.connect(self.showLog)
                self.train_thread.start()  # 启动线程
                self.showLog('正在加载数据...')
        except ValueError as e:
            QMessageBox.critical(self, "错误", f"输入参数无效: {e}")

    def showLog(self, message):
        self.showlog_text.append(message)
    #-------------------------------------------------测试部分--------------------------------------------------
    #导入测试图片
    def display_img(self, type,image_path):
        if type == 'srcimg':
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(self.srcImg_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.srcImg_label.setPixmap(scaled_pixmap)
        if type == 'predimg':
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(self.srcImg_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.preImg_label.setPixmap(scaled_pixmap)
    def importTestimg(self):
        image_path,_ = QFileDialog.getOpenFileName(self, "选择图片文件", "",
                                                   "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)")
        if image_path:
            self.testImgpath = image_path
            self.display_img('srcimg',image_path)
    #开始测试
    def startTest(self):
        try:
            image_path = self.testImgpath
            model_path = './runs/detect/{}/weights/best.pt'.format(Config.name)
            #model_path = ('model/detectionMVP.pt')
            pre_image, detections = self.test_image(image_path, model_path)
            self.display_img('predimg',pre_image)
        except Exception as e:
            QMessageBox.critical(self,'错误','请先训练模型并导入图片！')

    def test_image(self, image_path, model_path):
        model = YOLO(model_path)
        results = model(image_path)
        # Process results list
        for result in results:
            boxes = result.boxes  # Boxes object for bounding box outputs
            masks = result.masks  # Masks object for segmentation masks outputs
            keypoints = result.keypoints  # Keypoints object for pose outputs
            probs = result.probs  # Probs object for classification outputs
            obb = result.obb  # Oriented boxes object for OBB outputs
            names = result.names
            result.save(filename="./images/result.jpg")  # save to disk
        # 初始化空列表存储结果
        detections = []
        for box in result.boxes:
            # print(f"Class: {box.cls}, Confidence: {box.conf}, Box Coordinates: {box.xyxy}")
            class_id = int(box.cls)  # 类别ID（通常是整数）
            confidence = float(box.conf)  # 置信度（通常是浮点数）
            detections.append({
                "class_id": class_id,
                "confidence": confidence
            })
        pre_image = './images/result.jpg'
        # names:{0:'fish',1:'xzc'}
        detection_text = ""
        for i, detection in enumerate(detections):
            if i >= 6:  # 显示前6个物体
                break
            detection_text += f"类别名称: {names[detection['class_id']]}, 置信度: {detection['confidence']}\n"

        # 更新标签的文本，将结果显示在 self.additional_label 中
        print(detection_text)
        self.result_label.setText(detection_text)
        #检测仪表盘
        ybptext = showmaV(image_path)
        self.maV_label.setText(ybptext)
        return pre_image, detections

    def saveModel(self):
        if self.model is None:
            QMessageBox.critical(self,'警告','请先训练模型！')
            return
        else:
            # 打开文件保存对话框
            file_path, _ = QFileDialog.getSaveFileName(self, "保存模型权重", "", "pt 文件 (*.pt);;所有文件 (*.*)")
            if file_path:
                source = self.model
                destination = file_path
                shutil.copy(source, destination)
                # 显示信息框
                QMessageBox.information(self, "信息", "模型权重保存成功！")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()
