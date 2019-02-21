from guiboi import Ui_MainWindow
import os
import sys
import time
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import requests
import keyboard
from bs4 import BeautifulSoup


# http://speedtest.newark.linode.com/100MB-newark.bin
# 100mb.bin




class movebar1(QtCore.QThread):

    triggered = pyqtSignal()

    def __init__(self, url, filename, progressbarnum):
        QtCore.QThread.__init__(self)
        self.url = url
        self.filename = filename
        self.progressbarusing = progressbarnum
        self.completionbarvalue = 0
        self.finisheddownload = False

    def __del__(self):
        self.wait()

    def progressbarusing2(self):
        return self.progressbarusing

    def completionbarval(self):
        return self.completionbarvalue

    def run(self):
        try:
            previousvalue = 0.0
            with open(self.filename, 'wb') as f:
                response = requests.get(self.url, stream=True)
                total = response.headers.get('content-length')
                print(total)
                if total is None:
                    f.write(response.content)
                else:
                    downloaded = 0
                    total = int(total)
                    for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                        downloaded += len(data)
                        f.write(data)
                        outof100percent = round(downloaded / total, 1) * 100
                        if previousvalue != outof100percent:
                            print(outof100percent)
                            self.completionbarvalue = outof100percent
                            differenceby = outof100percent - previousvalue
                            for x in range(int(differenceby / 10)):
                                self.triggered.emit()
                                # print(differenceby)
                                print(int(differenceby / 10))
                            previousvalue += outof100percent - previousvalue
                        else:
                            pass
                        done = int(50*downloaded/total)

        except:
            print("Download not work")


class App(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.completed = 0
        self.downloaders = [0, 0]
        self.lineEdit.setFocus()

        self.pushButton.clicked.connect(self.movebarup)
        self.show()

    def movebarup(self):

        if self.downloaders[0] == 0:
            self.downloaders[0] = 1
            self.progressBar.setValue(0)
            completionbar = 0
            self.downloader = movebar1(
                self.lineEdit.text(), self.lineEdit_2.text(), 1)
            self.downloader.triggered.connect(lambda: self.move_by_increment(
                self.downloader.progressbarusing2(), self.downloader.completionbarval()))
            self.downloader.start()
        elif self.downloaders[1] == 0:
            self.downloaders[1] = 1
            self.downloader2 = movebar1(
                self.lineEdit.text(), self.lineEdit_2.text(), 2)
            self.downloader2.triggered.connect(lambda: self.move_by_increment(
                self.downloader2.progressbarusing2(), self.downloader2.completionbarval()))
            self.downloader2.start()
    def move_by_increment(self, progressbarnumber, completionbar):
        self.progressbarusing = progressbarnumber
        print(f"Received {progressbarnumber} through signal")
        print(F"Completion bar at {completionbar} received from signal")
        print(self.progressbarusing)
        if self.progressbarusing == 1:
            self.progressBar.setValue(completionbar)
            if completionbar == 100:
                print("finished download on download bar 1")
                self.downloaders[0] = 0
        elif self.progressbarusing == 2:
            self.progressBar_2.setValue(completionbar)
            if completionbar == 100:
                print("finished download on download bar 2")
                self.downloaders[1] == 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
