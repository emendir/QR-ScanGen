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


# from window import Ui_MainWindow
Ui_MainWindow, QMainWindow = loadUiType('ScanGen.ui')


class ScanGen(QMainWindow, Ui_MainWindow):
    data = ""
    update_qr_code = pyqtSignal()
    update_text = pyqtSignal()

    def __init__(self, ):
        super(ScanGen, self).__init__()
        self.setupUi(self)
        self.update_text.connect(self.UpdateText)
        self.update_qr_code.connect(self.UpdateQrCode)
        Thread(target=self.RunScanner, args=()).start()

    def UpdateQrCode(self):
        qr_code = GenerateQrCode(self.data)
        image = ImageQt(qr_code)
        self.qr_code_lbl.setPixmap(QtGui.QPixmap.fromImage(image))

    def UpdateText(self):
        self.text_txbx.setPlainText(self.data)

    def RunScanner(self):
        cap = cv2.VideoCapture(0)
        while True:
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


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main = ScanGen()
    main.show()
    sys.exit(app.exec_())
