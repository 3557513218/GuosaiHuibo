# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QStatusBar, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1249, 902)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.train_widget = QWidget(self.centralwidget)
        self.train_widget.setObjectName(u"train_widget")
        self.train_widget.setGeometry(QRect(20, 70, 461, 451))
        self.StartTrain = QGroupBox(self.train_widget)
        self.StartTrain.setObjectName(u"StartTrain")
        self.StartTrain.setGeometry(QRect(10, 230, 441, 191))
        self.gridLayout_3 = QGridLayout(self.StartTrain)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.startTrain_btn = QPushButton(self.StartTrain)
        self.startTrain_btn.setObjectName(u"startTrain_btn")

        self.gridLayout_3.addWidget(self.startTrain_btn, 0, 0, 1, 1)

        self.showlog_text = QTextEdit(self.StartTrain)
        self.showlog_text.setObjectName(u"showlog_text")

        self.gridLayout_3.addWidget(self.showlog_text, 1, 0, 1, 1)

        self.DataImport = QGroupBox(self.train_widget)
        self.DataImport.setObjectName(u"DataImport")
        self.DataImport.setGeometry(QRect(10, 10, 141, 201))
        self.gridLayout_2 = QGridLayout(self.DataImport)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.importData_btn = QPushButton(self.DataImport)
        self.importData_btn.setObjectName(u"importData_btn")

        self.verticalLayout.addWidget(self.importData_btn)

        self.importCls_btn = QPushButton(self.DataImport)
        self.importCls_btn.setObjectName(u"importCls_btn")

        self.verticalLayout.addWidget(self.importCls_btn)

        self.clsShow_text = QTextEdit(self.DataImport)
        self.clsShow_text.setObjectName(u"clsShow_text")

        self.verticalLayout.addWidget(self.clsShow_text)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.Parameters = QGroupBox(self.train_widget)
        self.Parameters.setObjectName(u"Parameters")
        self.Parameters.setGeometry(QRect(150, 10, 301, 191))
        self.gridLayout = QGridLayout(self.Parameters)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lr_label = QLabel(self.Parameters)
        self.lr_label.setObjectName(u"lr_label")

        self.gridLayout.addWidget(self.lr_label, 0, 0, 1, 1)

        self.epoch_label = QLabel(self.Parameters)
        self.epoch_label.setObjectName(u"epoch_label")

        self.gridLayout.addWidget(self.epoch_label, 0, 3, 1, 1)

        self.epoch_text = QLineEdit(self.Parameters)
        self.epoch_text.setObjectName(u"epoch_text")

        self.gridLayout.addWidget(self.epoch_text, 0, 4, 1, 1)

        self.bs_label = QLabel(self.Parameters)
        self.bs_label.setObjectName(u"bs_label")

        self.gridLayout.addWidget(self.bs_label, 1, 0, 1, 2)

        self.bs_text = QLineEdit(self.Parameters)
        self.bs_text.setObjectName(u"bs_text")

        self.gridLayout.addWidget(self.bs_text, 1, 2, 1, 1)

        self.prjName_label = QLabel(self.Parameters)
        self.prjName_label.setObjectName(u"prjName_label")

        self.gridLayout.addWidget(self.prjName_label, 1, 3, 1, 1)

        self.prjName_text = QLineEdit(self.Parameters)
        self.prjName_text.setObjectName(u"prjName_text")

        self.gridLayout.addWidget(self.prjName_text, 1, 4, 1, 1)

        self.lr_text = QLineEdit(self.Parameters)
        self.lr_text.setObjectName(u"lr_text")

        self.gridLayout.addWidget(self.lr_text, 0, 2, 1, 1)

        self.test_widget = QWidget(self.centralwidget)
        self.test_widget.setObjectName(u"test_widget")
        self.test_widget.setGeometry(QRect(500, 60, 671, 511))
        self.modelTest = QGroupBox(self.test_widget)
        self.modelTest.setObjectName(u"modelTest")
        self.modelTest.setGeometry(QRect(20, 10, 641, 521))
        self.layoutWidget = QWidget(self.modelTest)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(80, 20, 541, 271))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.srcImg_label = QLabel(self.layoutWidget)
        self.srcImg_label.setObjectName(u"srcImg_label")
        self.srcImg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.srcImg_label)

        self.preImg_label = QLabel(self.layoutWidget)
        self.preImg_label.setObjectName(u"preImg_label")
        self.preImg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.preImg_label)

        self.result_label = QLabel(self.modelTest)
        self.result_label.setObjectName(u"result_label")
        self.result_label.setGeometry(QRect(80, 300, 539, 81))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layoutWidget1 = QWidget(self.modelTest)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(100, 430, 501, 38))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.testImgImport_btn = QPushButton(self.layoutWidget1)
        self.testImgImport_btn.setObjectName(u"testImgImport_btn")

        self.horizontalLayout_2.addWidget(self.testImgImport_btn)

        self.startTest_btn = QPushButton(self.layoutWidget1)
        self.startTest_btn.setObjectName(u"startTest_btn")

        self.horizontalLayout_2.addWidget(self.startTest_btn)

        self.saveModel_btn = QPushButton(self.layoutWidget1)
        self.saveModel_btn.setObjectName(u"saveModel_btn")

        self.horizontalLayout_2.addWidget(self.saveModel_btn)

        self.maV_label = QLabel(self.modelTest)
        self.maV_label.setObjectName(u"maV_label")
        self.maV_label.setGeometry(QRect(80, 400, 539, 21))
        self.maV_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.showimg_label = QLabel(self.centralwidget)
        self.showimg_label.setObjectName(u"showimg_label")
        self.showimg_label.setGeometry(QRect(10, 530, 481, 221))
        self.showimg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u76ee\u6807\u68c0\u6d4b\u6a21\u578b\u8bad\u7ec3", None))
        self.StartTrain.setTitle(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u8bad\u7ec3", None))
        self.startTrain_btn.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u8bad\u7ec3", None))
        self.DataImport.setTitle(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u5bfc\u5165", None))
        self.importData_btn.setText(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u5bfc\u5165", None))
        self.importCls_btn.setText(QCoreApplication.translate("MainWindow", u"\u7c7b\u522b\u6587\u4ef6\u5bfc\u5165", None))
        self.Parameters.setTitle(QCoreApplication.translate("MainWindow", u"\u53c2\u6570\u8bbe\u7f6e", None))
        self.lr_label.setText(QCoreApplication.translate("MainWindow", u"\u5b66\u4e60\u7387\uff1a", None))
        self.epoch_label.setText(QCoreApplication.translate("MainWindow", u"\u8bad\u7ec3\u8f6e\u6b21\uff1a", None))
        self.epoch_text.setText("")
        self.bs_label.setText(QCoreApplication.translate("MainWindow", u"\u6279\u6b21\u5927\u5c0f\uff1a", None))
        self.prjName_label.setText(QCoreApplication.translate("MainWindow", u"\u9879\u76ee\u540d\u79f0\uff1a", None))
        self.prjName_text.setText("")
        self.modelTest.setTitle(QCoreApplication.translate("MainWindow", u"\u6a21\u578b\u6d4b\u8bd5", None))
        self.srcImg_label.setText(QCoreApplication.translate("MainWindow", u"\u539f\u59cb\u56fe\u50cf", None))
        self.preImg_label.setText(QCoreApplication.translate("MainWindow", u"\u9884\u6d4b\u7ed3\u679c", None))
        self.result_label.setText(QCoreApplication.translate("MainWindow", u"\u9884\u6d4b\u7ed3\u679c", None))
        self.testImgImport_btn.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165\u6d4b\u8bd5\u56fe\u7247", None))
        self.startTest_btn.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u6d4b\u8bd5", None))
        self.saveModel_btn.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u6a21\u578b", None))
        self.maV_label.setText("")
        self.showimg_label.setText("")
    # retranslateUi

