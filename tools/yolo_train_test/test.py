import argparse
import sys
import time

from PySide6.QtWidgets import QMainWindow, QApplication,QMessageBox,QFileDialog,QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt,QThread, Signal
from ui.ui_test import Ui_MainWindow
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))
from ultralytics import YOLO
import yaml
import json
from utils import genJson
class TestThread(QThread):
    result_signal = Signal(dict)
    show_signal = Signal(str)
    def __init__(self, modelpath,testpath,Ctype,dataset,app):
        super().__init__()
        self.modelpath = modelpath
        self.testpath = testpath
        self.ctype = Ctype
        self.dataset = dataset
        self.app = app

    def run(self):
        model = YOLO(self.modelpath)
        metrics = model.val(data="dataset_config_spw.yaml", save_json=False, plots=True, split="test",iou=0.2)
        self.result_signal.emit(metrics.results_dict)
        time.sleep(0.5)
        results = model.predict(source=self.testpath,save=True)
        if self.dataset == 0:
            get_type = lambda test_name: {"testA": "shengxian", "testB": "putong", "testC": "weixianpin"}.get(test_name,
                                                                                                "未知类型")
        elif self.dataset == 1:
            get_type = lambda test_name: {"testA": "paomo", "testB": "suliao", "testC": "zhixiang"}.get(test_name,
                                                                                                "未知类型")
        label = get_type(self.ctype)
        true_count=0
        false_count=0
        falseimgpath=[]
        for result in results:
            boxes = result.boxes  # Boxes object for bounding box outputs
            names = result.names
            print(names[int(boxes[0].cls)])
            if names[int(boxes[0].cls)] == label:
                true_count += 1
            else:
                false_count += 1
                falseimgpath.append(result.path)
        falseimgpath = str(falseimgpath)
        data = '图片总数:{} 正确预测数:{} 错误预测数:{}'.format(true_count+false_count,true_count,false_count)+ falseimgpath
        #self.app.allresults_label.append('图片总数:{} 正确预测数:{} 错误预测数:{}'.format(true_count+false_count,true_count,false_count)+ falseimgpath)
        #time.sleep(0.5)
        self.show_signal.emit(data)
        with open('metrics_results_{}.txt'.format(self.ctype), 'a', encoding='utf-8') as file:
            file.write("\n"+'图片总数:{} 正确预测数:{} 错误预测数:{},错误预测图像路径:{}'.format(true_count+false_count,true_count, false_count,falseimgpath))
        print(true_count,false_count,falseimgpath)
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self,folder_path):
        super().__init__()
        self.setupUi(self)
        self.imgpath = None
        self.modelpath = None
        self.testType = folder_path
        self.dataset_path = None
        self.predict_path = None
        self.datasettype = None
        self.A = None
        self.B = None
        self.C = None
        self.importImg_btn.clicked.connect(self.importImg)
        self.importModel_btn.clicked.connect(self.importModel)
        self.testImg_btn.clicked.connect(self.testImg)
        self.importSettings_btn.clicked.connect(self.importSettings)
        self.dicStartTest_btn.clicked.connect(self.testDic)
        self.importDataset_btn.clicked.connect(self.importDataset)
    def importDataset(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择数据集文件夹")
        if folder_path:
            self.dataset_path = folder_path  # 更新配置对象
            QMessageBox.information(self, "信息", f"数据集文件夹导入成功：{self.dataset_path}")
            genJson(self.dataset_path, ['weixianpin','putong','shengxian'],'dataset_config_spw.yaml')
            listpath = os.path.join(self.dataset_path, 'images/{}'.format(self.testType)).replace('\\','/')
            self.predict_path = listpath
            if not os.path.isdir(listpath):
                QMessageBox.critical(self,'提示','没有找到测试文件夹')
                return

            self.testDic_label.setText(listpath)
            if os.path.isdir(listpath):
                 files = os.listdir(listpath)
                 file_names = "\n".join(files)
                 self.testDic_label.append(file_names)
            print(listpath)
            self.update_test_folder(self.testType)
    def update_test_folder(self,X):
        # 读取原始 data.yaml 文件
        with open('dataset_config_spw.yaml', 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 修改 test 行
        for i, line in enumerate(lines):
            if line.startswith('test:'):
                lines[i] = f'test: images/{X}\n'
                break

        # 将更新后的内容写回 data.yaml 文件
        with open('dataset_config_spw.yaml', 'w', encoding='utf-8') as file:
            file.writelines(lines)
    def testDic(self):
        if not self.modelpath:
            QMessageBox.critical(self, '错误', '请先导入模型文件。')
            return
        self.thread = TestThread(self.modelpath,self.predict_path,self.testType,self.datasettype,self)
        self.thread.result_signal.connect(self.handle_results)
        self.thread.show_signal.connect(self.add_text)
        self.thread.start()
    def handle_results(self, results):
        str_results = str(results)
        self.metrics_label.clear()
        self.metrics_label.append(str_results)
        with open('metrics_results_{}.txt'.format(self.testType), 'w') as f:
            self.txt = 'metrics_results_{}.txt'.format(self.testType)
            json.dump(results, f, indent=4)
        QMessageBox.information(self, '提示', '测试结果已保存在 metrics_results_{}.txt'.format(self.testType))
    def add_text(self,data):
        self.allresults_label.append(data)

    def importSettings(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择 YAML 文件", "", "YAML Files (*.yaml *.yml)")
        if file_path:
            data_dict = self.load_yaml(file_path)
            QMessageBox.information(self, "加载成功", f"文件内容: {data_dict}")
            if '生鲜' in data_dict.keys():
                self.A=data_dict['生鲜']
                self.B=data_dict['普通']
                self.C=data_dict['加急']
                html_contentA = f'<img src="{"./images/1.png"}" width="25" height="25" style="vertical-align: middle;"> 生鲜分发'
                self.A_label.setText(html_contentA)  # 设置文本

                html_contentB = f'<img src="{"./images/2.png"}" width="25" height="25" style="vertical-align: middle;"> 普通分发'
                self.B_label.setText(html_contentB)  # 设置文本

                html_contentC = f'<img src="{"./images/3.png"}" width="25" height="25" style="vertical-align: middle;"> 加急分发'
                self.C_label.setText(html_contentC)  # 设置文本
                self.datasettype = 0
            if '泡沫' in data_dict.keys():
                self.A = data_dict['泡沫']
                self.B = data_dict['塑料']
                self.C = data_dict['纸箱']
                html_contentA = f'<img src="{"./images/1.png"}" width="25" height="25" style="vertical-align: middle;"> 泡沫分发'
                self.A_label.setText(html_contentA)  # 设置文本

                html_contentB = f'<img src="{"./images/2.png"}" width="25" height="25" style="vertical-align: middle;"> 塑料分发'
                self.B_label.setText(html_contentB)  # 设置文本

                html_contentC = f'<img src="{"./images/3.png"}" width="25" height="25" style="vertical-align: middle;"> 纸箱分发'
                self.C_label.setText(html_contentC)  # 设置文本
                self.datasettype = 1
    def load_yaml(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            print(data)
        return data
    def importImg(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图像文件", "",
                                                   "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)")
        if file_path:
            # 加载图像并显示在 QLabel 中
            pixmap = QPixmap(file_path)
            self.srcImg_label.setPixmap(pixmap.scaled(self.srcImg_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.imgpath = file_path
    def importModel(self):
        if self.A == None:
            QMessageBox.critical(self,'提示','请先导入配置文件')
            return
        file_path, _ = QFileDialog.getOpenFileName(self, "选择模型文件", "",
                                                   "PyTorch Models (*.pt);;All Files (*)")
        if file_path:
            try:
                QMessageBox.information(self, "成功", "模型加载成功！")
                model = YOLO(file_path)
                self.modelpath = file_path
                class_names = model.names
                dict_values = class_names.values()
                if not (self.A in dict_values and self.B in dict_values and self.C in dict_values):
                    QMessageBox.warning(self,'警告','yaml文件中的标签和模型标签不匹配\n')
            except Exception as e:
                QMessageBox.critical(self, "错误", f"模型加载失败：{str(e)}")
    def testImg(self):
        if self.imgpath:
            model = YOLO(self.modelpath)
            results = model(self.imgpath)
            for result in results:
                boxes = result.boxes  # Boxes object for bounding box outputs
                masks = result.masks  # Masks object for segmentation masks outputs
                keypoints = result.keypoints  # Keypoints object for pose outputs
                probs = result.probs  # Probs object for classification outputs
                obb = result.obb  # Oriented boxes object for OBB outputs
                names = result.names
                result.save(filename="./images/result.jpg")  # save to disk

                pixmap = QPixmap("./images/result.jpg")
                self.predImg_label.setPixmap(
                    pixmap.scaled(self.predImg_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                #在标签上展示预测类别和概率：

                detections = []
                for box in result.boxes:
                    # print(f"Class: {box.cls}, Confidence: {box.conf}, Box Coordinates: {box.xyxy}")
                    class_id = int(box.cls)  # 类别ID（通常是整数）
                    confidence = float(box.conf)  # 置信度（通常是浮点数）
                    detections.append({
                        "class_id": class_id,
                        "confidence": confidence
                    })
                detection_text = ""
                for i, detection in enumerate(detections):
                    if i >= 1:  # 只显示前三个物体
                        break
                    detection_text += f"类别名称: {names[detection['class_id']]}, 置信度: {detection['confidence']}\n"
                    self.result_label.setText(detection_text)
                     # 更新标签的文本，将结果显示在 self.additional_label 中
                    self.A_label.setStyleSheet("")
                    self.B_label.setStyleSheet("")
                    self.C_label.setStyleSheet("")
                    if names[detection['class_id']] == self.A:
                        self.A_label.setStyleSheet("background-color: yellow;")
                    if names[detection['class_id']] == self.B:
                        self.B_label.setStyleSheet("background-color: yellow;")
                    if names[detection['class_id']] == self.C:
                        self.C_label.setStyleSheet("background-color: yellow;")

        else:
             QMessageBox.information(self,'错误','请先导入模型和图片')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='YOLOv8 测试工具')
    parser.add_argument('--folder', type=str, help='指定文件夹路径',default='testA')
    args = parser.parse_args()

    app = QApplication(sys.argv)
    win = MainWindow(args.folder)
    win.show()
    sys.exit(app.exec())
