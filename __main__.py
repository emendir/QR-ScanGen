from PyQt5.QtWidgets import QFileDialog
import copy
from PIL.ImageQt import ImageQt
import qrcode
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
import pyperclip
import webbrowser
import platform

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


abs_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)))
if os.path.exists(os.path.join(abs_dir, 'ScanGen.ui')):
    os.chdir(abs_dir)
    Ui_MainWindow, QMainWindow = loadUiType('ScanGen.ui')
else:
    from ScanGen import Ui_MainWindow


class ScanGen(QMainWindow, Ui_MainWindow):
    data = ""
    update_qr_code = pyqtSignal()
    update_text = pyqtSignal()
    search_for_cameras = pyqtSignal()
    update_camera_list = pyqtSignal(list)

    camera_index = 0
    radio_buttons = []
    closing = False

    def __init__(self, ):
        super(ScanGen, self).__init__()
        self.setupUi(self)
        bundle_dir = getattr(
            sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        self.setWindowIcon(QtGui.QIcon(os.path.join(bundle_dir, 'Icon.svg')))
        self.setWindowTitle("QR ScanGen")

        self.update_text.connect(self.UpdateText)
        self.update_qr_code.connect(self.UpdateQrCode)
        self.search_for_cameras.connect(self.SearchForCameras)
        self.update_camera_list.connect(self.UpdateCameraList)
        self.qr_code_lbl.mousePressEvent = self.SaveQR_File

        Thread(target=self.RunScanner, args=()).start()
        # self.search_for_cameras.emit()
        print("ready")

    def UpdateQrCode(self):
        qr_code = self.GenerateQrCode(self.data)

        image = ImageQt(qr_code)
        self.qr_code_lbl.setPixmap(QtGui.QPixmap.fromImage(image))

    def UpdateText(self):
        self.text_txbx.setPlainText(self.data)

    def ListCameraPorts(self):
        """
        Test the ports and returns a tuple with the available ports and the ones that are working.
        """
        non_working_ports = []
        dev_port = 0
        working_ports = []
        available_ports = []
        # if there are more than 5 non working ports stop the testing.
        while len(non_working_ports) < 6:
            if dev_port == self.camera_index:
                print(f"Skipping port {dev_port} because it is in use.")
                working_ports.append(dev_port)
            else:
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
                        if self.camera_index == "":  # if Scanner currently doesn't know which camera to use
                            self.camera_index = dev_port
                    else:
                        print("Port %s for camera ( %s x %s) is present but does not read." %
                              (dev_port, h, w))
                        available_ports.append(dev_port)
            dev_port += 1
        return available_ports, working_ports, non_working_ports

    def ChangeCamera(self, e):
        self.camera_index = self.sender().cv2_index
    testing_camera_ports = False

    def SearchForCameras(self):
        if self.testing_camera_ports:
            return
        self.testing_camera_ports = True

        def _search_for_cameras():
            working_cameras = self.ListCameraPorts()[1]
            self.update_camera_list.emit(working_cameras)
            self.testing_camera_ports = False
        Thread(target=_search_for_cameras, args=()).start()

    def UpdateCameraList(self, working_cameras: list):
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

    def RunScanner(self):
        # if self.camera_index == "":
        #     self.camera_index = 0
        while True:  # camera usage session loop (new iteration only when user changes camera)
            if self.closing:
                return
            current_camera = copy.deepcopy(self.camera_index)
            cap = cv2.VideoCapture(self.camera_index)
            self.search_for_cameras.emit()

            try:
                while True:
                    if self.closing:
                        return
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
                            Thread(target=self.AnalyseCode, args=()).start()
                            pyperclip.copy(self.data)
                    else:
                        if self.text_txbx.toPlainText() != self.data:

                            self.data = self.text_txbx.toPlainText()
                            self.update_qr_code.emit()
                    self.camera_image = QtGui.QImage(
                        frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
                    self.scanner_video_lbl.setPixmap(QtGui.QPixmap.fromImage(self.camera_image))

                    code = cv2.waitKey(10)
                    if code == ord('q'):
                        break
            except:
                print(f"Error working with camera {self.camera_index}")
                self.camera_index = ""
                self.search_for_cameras.emit()
                while self.camera_index == "":
                    print("waiting for camera")
                    time.sleep(0.1)

                # self.SearchForCameras()

    def AnalyseCode(self):
        # WIFI analysis
        elements = [e.split(":") for e in self.data.split(";")]
        if len(elements) > 2 and elements[0][0] == "WIFI" and elements[0][1] == "S" and elements[1][0] == "T" and elements[2][0] == "P":
            ssid = elements[0][2]
            type = elements[1][1]
            password = elements[2][1]

            import pywifi

            profile = pywifi.Profile()
            profile.ssid = ssid
            profile.auth = pywifi.const.AUTH_ALG_OPEN
            if type == "" or type.lower == "none":
                profile.akm.append(pywifi.const.AKM_TYPE_NONE)
            if type == "WPA":
                profile.akm.append(pywifi.const.AKM_TYPE_WPA)
            if type == "WPAPSK":
                profile.akm.append(pywifi.const.AKM_TYPE_WPAPSK)
            if type == "WPA2":
                profile.akm.append(pywifi.const.AKM_TYPE_WPA2)
            if type == "WPA2PSK":
                profile.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)
            # profile.cipher = pywifi.const.CIPHER_TYPE_CCMP
            profile.key = password

            try:
                wifi = pywifi.PyWiFi()
                iface = wifi.interfaces()[0]
                profile = iface.add_network_profile(profile)
                iface.connect(profile)
            except PermissionError:
                # handling permission denied error on linux
                if platform.system() == 'Linux':
                    os.system(f"nmcli dev wifi connect '{ssid}' password '{password}'")

        if IsWebsite(self.data):
            webbrowser.open_new_tab(self.data)

    def GenerateQrCode(self, text):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=3,
            border=4,   # number of pixels is  this * box_size
        )
        qr.add_data(text)   # give QRCode object our text to encode
        qr.make(fit=True)   # generate QR code from our text
        # we would like our QR code to be about as high as the camera image displayed
        desired_height = self.camera_image.height()
        # get the number of squares along an edge of the QR code
        qr_height_squares = len(qr.get_matrix())
        # calculate how many pixels should be used to display one square of the QR code
        qr.box_size = int((desired_height)/(qr_height_squares+2*qr.border))
        return qr.make_image()  # generate and return QR code image

    def closeEvent(self, event):
        self.closing = True
        event.accept()

    def SaveQR_File(self, eventargs):
        """Saves the currently displayed QR-Code to a file,
        after opening a file dialog asking the user for the file path"""
        filepath, ok = QFileDialog.getSaveFileName(
            self, 'Save QR Code', "", ("Images (*.png)"))
        if filepath:
            if filepath[-4:].lower() != ".png":
                print(filepath[-4:].lower())
                filepath += ".png"
            self.qr_code_lbl.pixmap().save(filepath)


def IsWebsite(text):
    return text.startswith("https://") or text.startswith("http://")


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main = ScanGen()
    main.show()
    sys.exit(app.exec_())
