# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'face_match.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(672, 763)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.face_register = QtWidgets.QPushButton(self.centralwidget)
        self.face_register.setGeometry(QtCore.QRect(50, 20, 121, 41))
        self.face_register.setObjectName("face_register")
        self.face_match = QtWidgets.QPushButton(self.centralwidget)
        self.face_match.setGeometry(QtCore.QRect(200, 20, 121, 41))
        self.face_match.setObjectName("face_match")
        self.face_search = QtWidgets.QPushButton(self.centralwidget)
        self.face_search.setGeometry(QtCore.QRect(350, 20, 121, 41))
        self.face_search.setObjectName("face_search")
        self.face_manage = QtWidgets.QPushButton(self.centralwidget)
        self.face_manage.setGeometry(QtCore.QRect(500, 20, 121, 41))
        self.face_manage.setObjectName("face_manage")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 84, 631, 601))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/images/c.jpg"))
        self.label.setIndent(3)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 672, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.face_register.setText(_translate("MainWindow", "信息录入"))
        self.face_match.setText(_translate("MainWindow", "人脸识别"))
        self.face_search.setText(_translate("MainWindow", "信息查询"))
        self.face_manage.setText(_translate("MainWindow", "信息管理"))



