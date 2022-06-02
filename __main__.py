import copy
import traceback
from PIL.ImageQt import ImageQt
import qrcode
import math
import pyqrcode
from threading import Thread
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUiType
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PyQt5.QtCore import pyqtSignal
import time
import os
if __file__ and os.path.exists(__file__):
    os.chdir(os.path.dirname(__file__))


def QR_Decoder(image):
    gray_img = cv2.cvtColor(image, 0)
    qr_code = decode(gray_img)

    for obj in qr_code:
        points = obj.polygon
        (x, y, w, h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        cv2.putText(image, obj.data.decode(), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        return {"image": image, "type": obj.type, "data": obj.data}


def GenerateQrCode(text):
    return qrcode.make(text)


def ListCameraPorts():
    """
    Test the ports and returns a tuple with the available ports and the ones that are working.
    """
    non_working_ports = []
    dev_port = 0
    working_ports = []
    available_ports = []
    # if there are more than 5 non working ports stop the testing.
    while len(non_working_ports) < 6:
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            non_working_ports.append(dev_port)
            print("Port %s is not working." % dev_port)
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                print("Port %s is working and reads images (%s x %s)" % (dev_port, h, w))
                working_ports.append(dev_port)
            else:
                print("Port %s for camera ( %s x %s) is present but does not reads." % (dev_port, h, w))
                available_ports.append(dev_port)
        dev_port += 1
    return available_ports, working_ports, non_working_ports


# from window import Ui_MainWindow
Ui_MainWindow, QMainWindow = loadUiType('ScanGen.ui')


class ScanGen(QMainWindow, Ui_MainWindow):
    data = ""
    update_qr_code = pyqtSignal()
    update_text = pyqtSignal()
    update_camera_list = pyqtSignal()
    camera_index = 0
    radio_buttons = []

    def __init__(self, ):
        super(ScanGen, self).__init__()
        self.setupUi(self)
        self.update_text.connect(self.UpdateText)
        self.update_qr_code.connect(self.UpdateQrCode)
        self.update_camera_list.connect(self.UpdateCameraList)
        self.UpdateCameraList()
        Thread(target=self.RunScanner, args=()).start()
        print("ready")

    def UpdateQrCode(self):
        qr_code = GenerateQrCode(self.data)
        image = ImageQt(qr_code)
        self.qr_code_lbl.setPixmap(QtGui.QPixmap.fromImage(image))

    def UpdateText(self):
        self.text_txbx.setPlainText(self.data)

    def RunScanner(self):
        while True:  # camera usage session loop (new iteration only when user changes camera)
            while(self.testing_camera_ports):   # wait while we look up camera ports
                time.sleep(0.1)
            current_camera = copy.deepcopy(self.camera_index)
            cap = cv2.VideoCapture(self.camera_index)
            try:
                while True:
                    if current_camera != self.camera_index:
                        break
                    ret, frame = cap.read()
                    result = QR_Decoder(frame)
                    if result is not None:
                        frame = result["image"]
                        data = result["data"].decode()
                        if data != self.data:
                            self.data = data
                            self.update_text.emit()
                            self.update_qr_code.emit()
                    else:
                        if self.text_txbx.toPlainText() != self.data:

                            self.data = self.text_txbx.toPlainText()
                            self.update_qr_code.emit()
                    image = QtGui.QImage(
                        frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
                    self.scanner_video_lbl.setPixmap(QtGui.QPixmap.fromImage(image))

                    code = cv2.waitKey(10)
                    if code == ord('q'):
                        break
            except:
                self.update_camera_list.emit()
                # self.UpdateCameraList()

    def ChangeCamera(self, e):
        self.camera_index = self.sender().cv2_index
    testing_camera_ports = False

    def UpdateCameraList(self):
        self.testing_camera_ports = True
        working_cameras = ListCameraPorts()[1]
        if self.camera_index not in working_cameras:
            self.camera_index = working_cameras[0]
        for radio_button in self.radio_buttons:
            try:
                radio_button.deleteLater()
            except:
                pass
        for i in working_cameras:
            radio_button = QtWidgets.QRadioButton(str(i), self.right_frame)
            radio_button.cv2_index = i
            if i == self.camera_index:
                radio_button.setChecked(True)
            radio_button.clicked.connect(self.ChangeCamera)
            self.right_frame_lyt.addWidget(radio_button)
            self.radio_buttons.append(radio_button)
        self.testing_camera_ports = False


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main = ScanGen()
    main.show()
    sys.exit(app.exec_())
