# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(767, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_6 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.labelImage = QLabel(self.centralwidget)
        self.labelImage.setObjectName(u"labelImage")
        self.labelImage.setMinimumSize(QSize(320, 240))

        self.verticalLayout_6.addWidget(self.labelImage)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btnConnectCamera = QPushButton(self.groupBox)
        self.btnConnectCamera.setObjectName(u"btnConnectCamera")
        self.btnConnectCamera.setMinimumSize(QSize(0, 50))

        self.horizontalLayout_2.addWidget(self.btnConnectCamera)

        self.btnCloseCamera = QPushButton(self.groupBox)
        self.btnCloseCamera.setObjectName(u"btnCloseCamera")
        self.btnCloseCamera.setMinimumSize(QSize(0, 50))

        self.horizontalLayout_2.addWidget(self.btnCloseCamera)

        self.labelConnectState = QLabel(self.groupBox)
        self.labelConnectState.setObjectName(u"labelConnectState")

        self.horizontalLayout_2.addWidget(self.labelConnectState)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.btnDeg1Down = QPushButton(self.groupBox)
        self.btnDeg1Down.setObjectName(u"btnDeg1Down")

        self.gridLayout.addWidget(self.btnDeg1Down, 2, 1, 1, 1)

        self.btnDeg1Up = QPushButton(self.groupBox)
        self.btnDeg1Up.setObjectName(u"btnDeg1Up")

        self.gridLayout.addWidget(self.btnDeg1Up, 2, 0, 1, 1)

        self.currDeg1 = QSpinBox(self.groupBox)
        self.currDeg1.setObjectName(u"currDeg1")
        self.currDeg1.setFrame(True)
        self.currDeg1.setReadOnly(False)
        self.currDeg1.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.currDeg1.setMinimum(-180)
        self.currDeg1.setMaximum(180)
        self.currDeg1.setStepType(QAbstractSpinBox.DefaultStepType)

        self.gridLayout.addWidget(self.currDeg1, 1, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)

        self.currDeg2 = QSpinBox(self.groupBox)
        self.currDeg2.setObjectName(u"currDeg2")
        self.currDeg2.setFrame(True)
        self.currDeg2.setReadOnly(False)
        self.currDeg2.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.currDeg2.setMinimum(-180)
        self.currDeg2.setMaximum(180)
        self.currDeg2.setStepType(QAbstractSpinBox.DefaultStepType)

        self.gridLayout_2.addWidget(self.currDeg2, 1, 1, 1, 1)

        self.btnDeg2Up = QPushButton(self.groupBox)
        self.btnDeg2Up.setObjectName(u"btnDeg2Up")

        self.gridLayout_2.addWidget(self.btnDeg2Up, 2, 0, 1, 1)

        self.btnDeg2Down = QPushButton(self.groupBox)
        self.btnDeg2Down.setObjectName(u"btnDeg2Down")

        self.gridLayout_2.addWidget(self.btnDeg2Down, 2, 1, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.horizontalLayout_4.addWidget(self.groupBox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.btnSetSavePath = QPushButton(self.groupBox_2)
        self.btnSetSavePath.setObjectName(u"btnSetSavePath")

        self.horizontalLayout_3.addWidget(self.btnSetSavePath)

        self.lineEditSavePath = QLineEdit(self.groupBox_2)
        self.lineEditSavePath.setObjectName(u"lineEditSavePath")
        self.lineEditSavePath.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_3.addWidget(self.lineEditSavePath)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.labelCurrImgNum = QLabel(self.groupBox_2)
        self.labelCurrImgNum.setObjectName(u"labelCurrImgNum")

        self.gridLayout_3.addWidget(self.labelCurrImgNum, 0, 1, 1, 1)

        self.comboBoxType = QComboBox(self.groupBox_2)
        self.comboBoxType.addItem("")
        self.comboBoxType.addItem("")
        self.comboBoxType.addItem("")
        self.comboBoxType.addItem("")
        self.comboBoxType.setObjectName(u"comboBoxType")

        self.gridLayout_3.addWidget(self.comboBoxType, 0, 0, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout_3)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        self.btnSaveImage = QPushButton(self.groupBox_2)
        self.btnSaveImage.setObjectName(u"btnSaveImage")
        self.btnSaveImage.setMinimumSize(QSize(100, 50))

        self.verticalLayout_5.addWidget(self.btnSaveImage)


        self.horizontalLayout_4.addWidget(self.groupBox_2)

        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(2, 1)

        self.verticalLayout_6.addLayout(self.horizontalLayout_4)

        self.verticalLayout_6.setStretch(0, 2)
        self.verticalLayout_6.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u4e91\u53f0\u76f8\u673a\u52a9\u624b HuiBo.Robot", None))
        self.labelImage.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u4e91\u53f0\u63a7\u5236", None))
        self.btnConnectCamera.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5\u76f8\u673a", None))
        self.btnCloseCamera.setText(QCoreApplication.translate("MainWindow", u"\u5173\u95ed\u8fde\u63a5", None))
        self.labelConnectState.setText(QCoreApplication.translate("MainWindow", u"\u672a\u8fde\u63a5", None))
        self.btnDeg1Down.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.btnDeg1Up.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u6c34\u5e73\u89d2\u5ea6:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u5782\u76f4\u89d2\u5ea6:", None))
        self.btnDeg2Up.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.btnDeg2Down.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u56fe\u7247\u91c7\u96c6", None))
        self.btnSetSavePath.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e\u4fdd\u5b58\u8def\u5f84", None))
        self.labelCurrImgNum.setText(QCoreApplication.translate("MainWindow", u"\u5df2\u91c7\u96c6\u6570\u91cf:0", None))
        self.comboBoxType.setItemText(0, QCoreApplication.translate("MainWindow", u"\u539f\u59cb\u5206\u8fa8\u7387", None))
        self.comboBoxType.setItemText(1, QCoreApplication.translate("MainWindow", u"1920x1080", None))
        self.comboBoxType.setItemText(2, QCoreApplication.translate("MainWindow", u"680x480", None))
        self.comboBoxType.setItemText(3, QCoreApplication.translate("MainWindow", u"320x240", None))

        self.btnSaveImage.setText(QCoreApplication.translate("MainWindow", u"\u91c7\u96c6\u56fe\u7247", None))
    # retranslateUi

