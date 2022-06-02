# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ScanGen.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.images_frm = QtWidgets.QFrame(self.centralwidget)
        self.images_frm.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.images_frm.setFrameShadow(QtWidgets.QFrame.Raised)
        self.images_frm.setObjectName("images_frm")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.images_frm)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scanner_video_lbl = QtWidgets.QLabel(self.images_frm)
        self.scanner_video_lbl.setText("")
        self.scanner_video_lbl.setObjectName("scanner_video_lbl")
        self.horizontalLayout.addWidget(self.scanner_video_lbl)
        self.right_frame = QtWidgets.QFrame(self.images_frm)
        self.right_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.right_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.right_frame.setObjectName("right_frame")
        self.right_frame_lyt = QtWidgets.QVBoxLayout(self.right_frame)
        self.right_frame_lyt.setObjectName("right_frame_lyt")
        self.qr_code_lbl = QtWidgets.QLabel(self.right_frame)
        self.qr_code_lbl.setText("")
        self.qr_code_lbl.setObjectName("qr_code_lbl")
        self.right_frame_lyt.addWidget(self.qr_code_lbl)
        self.label = QtWidgets.QLabel(self.right_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label.setObjectName("label")
        self.right_frame_lyt.addWidget(self.label)
        self.horizontalLayout.addWidget(self.right_frame)
        self.verticalLayout.addWidget(self.images_frm)
        self.text_txbx = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.text_txbx.setMaximumSize(QtCore.QSize(16777215, 200))
        self.text_txbx.setObjectName("text_txbx")
        self.verticalLayout.addWidget(self.text_txbx)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
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
        self.label.setText(_translate("MainWindow", "Available Cameras:"))
