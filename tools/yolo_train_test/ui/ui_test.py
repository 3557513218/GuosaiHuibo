# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QStatusBar, QTabWidget, QTextEdit,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1086, 853)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(0, 0))
        MainWindow.setMaximumSize(QSize(4144444, 444444))
        MainWindow.setStyleSheet(u"QLabel,  QLineEdit {\n"
"    font-size: 15px; /* \u6839\u636e\u9700\u8981\u8c03\u6574\u5b57\u4f53\u5927\u5c0f */\n"
"    font-weight: bold;\n"
"    color: #00BFFF  /* \u4f7f\u7528\u6d45\u84dd\u8272 */\n"
"}\n"
"QMainWindow{\n"
"background-color: #2c3e50\n"
"}\n"
"QPushButton {\n"
"    font-family: 'Roboto';\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"    color: #00BFFF; /* \u6d45\u84dd\u8272\u5b57\u4f53 */\n"
"    background-color: #1E1E1E; /* \u6df1\u8272\u80cc\u666f */\n"
"    border: 2px solid #00BFFF; /* \u6d45\u84dd\u8272\u8fb9\u6846 */\n"
"    border-radius: 10px; /* \u5706\u89d2 */\n"
"    padding: 8px 16px; /* \u5185\u8fb9\u8ddd\uff0c\u589e\u5927\u70b9\u51fb\u533a\u57df */\n"
"}\n"
"\n"
"/* \u9f20\u6807\u60ac\u505c\u6548\u679c */\n"
"QPushButton:hover {\n"
"    background-color: #00BFFF; /* \u60ac\u505c\u65f6\u80cc\u666f\u53d8\u4e3a\u6d45\u84dd\u8272 */\n"
"    color: #1E1E1E; /* \u60ac\u505c\u65f6\u5b57\u4f53\u989c\u8272\u53d8\u4e3a\u6df1\u8272 */\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u6548\u679c"
                        " */\n"
"QPushButton:pressed {\n"
"    background-color: #0080FF; /* \u6309\u4e0b\u65f6\u80cc\u666f\u53d8\u4e3a\u6df1\u84dd\u8272 */\n"
"    border: 2px solid #0080FF; /* \u6309\u4e0b\u65f6\u8fb9\u6846\u53d8\u4e3a\u6df1\u84dd\u8272 */\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.importSettings_btn = QPushButton(self.centralwidget)
        self.importSettings_btn.setObjectName(u"importSettings_btn")
        self.importSettings_btn.setGeometry(QRect(30, 30, 141, 61))
        self.importSettings_btn.setStyleSheet(u"")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(120, 110, 881, 681))
        self.tabWidget.setStyleSheet(u"QPushButton {\n"
"    font-family: 'Roboto';\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"    color: #00BFFF; /* \u6d45\u84dd\u8272\u5b57\u4f53 */\n"
"    background-color: #1E1E1E; /* \u6df1\u8272\u80cc\u666f */\n"
"    border: 2px solid #00BFFF; /* \u6d45\u84dd\u8272\u8fb9\u6846 */\n"
"    border-radius: 10px; /* \u5706\u89d2 */\n"
"    padding: 8px 16px; /* \u5185\u8fb9\u8ddd\uff0c\u589e\u5927\u70b9\u51fb\u533a\u57df */\n"
"}\n"
"\n"
"/* \u9f20\u6807\u60ac\u505c\u6548\u679c */\n"
"QPushButton:hover {\n"
"    background-color: #00BFFF; /* \u60ac\u505c\u65f6\u80cc\u666f\u53d8\u4e3a\u6d45\u84dd\u8272 */\n"
"    color: #1E1E1E; /* \u60ac\u505c\u65f6\u5b57\u4f53\u989c\u8272\u53d8\u4e3a\u6df1\u8272 */\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u6548\u679c */\n"
"QPushButton:pressed {\n"
"    background-color: #0080FF; /* \u6309\u4e0b\u65f6\u80cc\u666f\u53d8\u4e3a\u6df1\u84dd\u8272 */\n"
"    border: 2px solid #0080FF; /* \u6309\u4e0b\u65f6\u8fb9\u6846\u53d8\u4e3a\u6df1\u84dd\u8272 */\n"
"}")
        self.SingleTest = QWidget()
        self.SingleTest.setObjectName(u"SingleTest")
        self.srcImg_label = QLabel(self.SingleTest)
        self.srcImg_label.setObjectName(u"srcImg_label")
        self.srcImg_label.setGeometry(QRect(10, 10, 400, 300))
        font = QFont()
        font.setBold(True)
        font.setItalic(False)
        self.srcImg_label.setFont(font)
        self.srcImg_label.setStyleSheet(u"border: 1px solid black; /* \u9ed1\u8272\u5b9e\u7ebf\u8fb9\u6846 */\n"
"padding: 5px; /* \u5185\u8fb9\u8ddd */")
        self.srcImg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.predImg_label = QLabel(self.SingleTest)
        self.predImg_label.setObjectName(u"predImg_label")
        self.predImg_label.setGeometry(QRect(420, 10, 400, 300))
        font1 = QFont()
        font1.setBold(True)
        self.predImg_label.setFont(font1)
        self.predImg_label.setStyleSheet(u"border: 1px solid black; /* \u9ed1\u8272\u5b9e\u7ebf\u8fb9\u6846 */\n"
"padding: 5px; /* \u5185\u8fb9\u8ddd */")
        self.predImg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label = QLabel(self.SingleTest)
        self.result_label.setObjectName(u"result_label")
        self.result_label.setGeometry(QRect(130, 380, 591, 51))
        self.result_label.setFont(font1)
        self.result_label.setStyleSheet(u"border: 1px solid black; /* \u9ed1\u8272\u5b9e\u7ebf\u8fb9\u6846 */\n"
"padding: 5px; /* \u5185\u8fb9\u8ddd */")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.importModel_btn = QPushButton(self.SingleTest)
        self.importModel_btn.setObjectName(u"importModel_btn")
        self.importModel_btn.setGeometry(QRect(150, 490, 151, 51))
        self.importModel_btn.setStyleSheet(u"QPushButton {\n"
"    font-family: 'Roboto';\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"    color: #00BFFF; /* \u6d45\u84dd\u8272\u5b57\u4f53 */\n"
"    background-color: #1E1E1E; /* \u6df1\u8272\u80cc\u666f */\n"
"    border: 2px solid #00BFFF; /* \u6d45\u84dd\u8272\u8fb9\u6846 */\n"
"    border-radius: 10px; /* \u5706\u89d2 */\n"
"    padding: 8px 16px; /* \u5185\u8fb9\u8ddd\uff0c\u589e\u5927\u70b9\u51fb\u533a\u57df */\n"
"}\n"
"\n"
"/* \u9f20\u6807\u60ac\u505c\u6548\u679c */\n"
"QPushButton:hover {\n"
"    background-color: #00BFFF; /* \u60ac\u505c\u65f6\u80cc\u666f\u53d8\u4e3a\u6d45\u84dd\u8272 */\n"
"    color: #1E1E1E; /* \u60ac\u505c\u65f6\u5b57\u4f53\u989c\u8272\u53d8\u4e3a\u6df1\u8272 */\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u6548\u679c */\n"
"QPushButton:pressed {\n"
"    background-color: #0080FF; /* \u6309\u4e0b\u65f6\u80cc\u666f\u53d8\u4e3a\u6df1\u84dd\u8272 */\n"
"    border: 2px solid #0080FF; /* \u6309\u4e0b\u65f6\u8fb9\u6846\u53d8\u4e3a\u6df1\u84dd\u8272 */\n"
"}")
        self.importImg_btn = QPushButton(self.SingleTest)
        self.importImg_btn.setObjectName(u"importImg_btn")
        self.importImg_btn.setGeometry(QRect(340, 490, 141, 51))
        self.importImg_btn.setStyleSheet(u"")
        self.testImg_btn = QPushButton(self.SingleTest)
        self.testImg_btn.setObjectName(u"testImg_btn")
        self.testImg_btn.setGeometry(QRect(510, 490, 151, 51))
        self.testImg_btn.setStyleSheet(u"")
        self.A_label = QLabel(self.SingleTest)
        self.A_label.setObjectName(u"A_label")
        self.A_label.setGeometry(QRect(220, 580, 111, 51))
        self.A_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.B_label = QLabel(self.SingleTest)
        self.B_label.setObjectName(u"B_label")
        self.B_label.setGeometry(QRect(360, 580, 111, 51))
        self.B_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.C_label = QLabel(self.SingleTest)
        self.C_label.setObjectName(u"C_label")
        self.C_label.setGeometry(QRect(490, 580, 111, 51))
        self.C_label.setScaledContents(True)
        self.C_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tabWidget.addTab(self.SingleTest, "")
        self.DecTest = QWidget()
        self.DecTest.setObjectName(u"DecTest")
        self.testDic_label = QTextEdit(self.DecTest)
        self.testDic_label.setObjectName(u"testDic_label")
        self.testDic_label.setGeometry(QRect(440, 100, 361, 351))
        self.testDic_label.setReadOnly(True)
        self.dicStartTest_btn = QPushButton(self.DecTest)
        self.dicStartTest_btn.setObjectName(u"dicStartTest_btn")
        self.dicStartTest_btn.setGeometry(QRect(160, 340, 141, 51))
        self.dicStartTest_btn.setStyleSheet(u"")
        self.importDataset_btn = QPushButton(self.DecTest)
        self.importDataset_btn.setObjectName(u"importDataset_btn")
        self.importDataset_btn.setGeometry(QRect(160, 170, 141, 51))
        self.importDataset_btn.setStyleSheet(u"")
        self.allresults_label = QTextEdit(self.DecTest)
        self.allresults_label.setObjectName(u"allresults_label")
        self.allresults_label.setGeometry(QRect(360, 480, 501, 141))
        self.metrics_label = QTextEdit(self.DecTest)
        self.metrics_label.setObjectName(u"metrics_label")
        self.metrics_label.setGeometry(QRect(30, 480, 271, 141))
        self.tabWidget.addTab(self.DecTest, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.tabWidget.raise_()
        self.importSettings_btn.raise_()
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u76ee\u6807\u68c0\u6d4b\u6a21\u578b\u8bad\u7ec3", None))
        self.importSettings_btn.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165\u914d\u7f6e\u6587\u4ef6", None))
        self.srcImg_label.setText(QCoreApplication.translate("MainWindow", u"\u672c\u5730\u56fe\u50cf", None))
        self.predImg_label.setText(QCoreApplication.translate("MainWindow", u"\u9884\u6d4b\u56fe\u50cf", None))
        self.result_label.setText(QCoreApplication.translate("MainWindow", u"\u9884\u6d4b\u7ed3\u679c\uff1a", None))
        self.importModel_btn.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165\u6a21\u578b", None))
        self.importImg_btn.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165\u672c\u5730\u56fe\u7247", None))
        self.testImg_btn.setText(QCoreApplication.translate("MainWindow", u"\u6d4b\u8bd5\u56fe\u7247", None))
        self.A_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
        self.B_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
        self.C_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.SingleTest), QCoreApplication.translate("MainWindow", u"\u5355\u5f20\u56fe\u7247\u6d4b\u8bd5", None))
        self.dicStartTest_btn.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u6d4b\u8bd5", None))
        self.importDataset_btn.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165\u6570\u636e\u96c6", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.DecTest), QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u5939\u6d4b\u8bd5", None))
    # retranslateUi

