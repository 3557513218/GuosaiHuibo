# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sub.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QWidget)

class Ui_subWindow(object):
    def setupUi(self, subWindow):
        if not subWindow.objectName():
            subWindow.setObjectName(u"subWindow")
        subWindow.resize(800, 600)
        self.centralwidget = QWidget(subWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(350, 210, 52, 14))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(330, 300, 75, 23))
        subWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(subWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 20))
        subWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(subWindow)
        self.statusbar.setObjectName(u"statusbar")
        subWindow.setStatusBar(self.statusbar)

        self.retranslateUi(subWindow)

        QMetaObject.connectSlotsByName(subWindow)
    # setupUi

    def retranslateUi(self, subWindow):
        subWindow.setWindowTitle(QCoreApplication.translate("subWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("subWindow", u"\u5b50\u7a97\u53e3", None))
        self.pushButton.setText(QCoreApplication.translate("subWindow", u"\u5173\u95ed\u7a97\u53e3", None))
    # retranslateUi

