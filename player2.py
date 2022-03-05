from ffpyplayer.player import MediaPlayer

from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import threading
import time
import cv2
from PIL import Image
import numpy
import os

class VideoPlayer:
    def __init__(self, filename,volume = 1.0):
        if not os.path.exists(filename):raise FileNotFound(filename)
        self.close = False
        self.state = None
        self.frame = None
        self.l=None
        self.filename = filename
        self.skip_interval=5

        self.player = MediaPlayer(filename, ff_opts={'sync': 'audio', 'paused': False, 'volume': volume, 't': 1e7+1, 'ss': 0})
        time.sleep(1)
        self.duration=self.player.get_metadata()['duration']
        handler_thread = threading.Thread(target=self.play, args=(), daemon=True)
        handler_thread.start()

    def play(self):
        while True:
            frame, self.val = self.player.get_frame()
            if self.val == 'eof':self.close=True
            if self.close == True:
                self.player.toggle_pause()
                self.player.close_player()
                time.sleep(2)
                break

            if isinstance(self.val, str) or self.val == 0.0:waitkey = 32
            else:waitkey = int(self.val * 100)
            pressed_key = cv2.waitKey(waitkey) & 0xFF

            if frame is None:continue

            image, pts = frame
            self.frame = (image, self.val)
            x, y = image.get_size()
            data = image.to_bytearray()[0]
            image =  Image.frombytes("RGB", (x, y), bytes(data))
            image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
            self.frame=frame

            if self.l!=None:
                h, w, ch = image.shape
                Image2 = QImage(image.data, w, h, ch * w, QImage.Format_RGB888)
                self.pixmap=QPixmap.fromImage(Image2)
                self.l.setPixmap(self.pixmap)
                self.l.setFixedWidth(self.l.pixmap().width())
                self.l.setFixedHeight(self.l.pixmap().height())
                self.l.parent().update()
            del image


    def seek_p(self):
            if int(self.player.get_pts()) + self.skip_interval < int(self.duration):
                self.player.seek(self.skip_interval, relative=True, accurate=False)
    def seek_m(self):
        if int(self.player.get_pts()) - self.skip_interval > 0:
            self.player.seek(-self.skip_interval, relative=True, accurate=False)



class ed(QWidget):
    def __init__(self,parent=None):
        super().__init__()
        vl=QVBoxLayout()
        self.setLayout(vl)
        pb=QPushButton('play');vl.addWidget(pb);pb.clicked.connect(self.play)
        pb=QPushButton('stop');vl.addWidget(pb);pb.clicked.connect(self.close)
        pb=QPushButton('pause');vl.addWidget(pb);pb.clicked.connect(self.pause)
        pb=QPushButton('seek+');vl.addWidget(pb);pb.clicked.connect(self.seek_p)
        pb=QPushButton('seek-');vl.addWidget(pb);pb.clicked.connect(self.seek_m)
        pb=QPushButton('mute');vl.addWidget(pb);pb.clicked.connect(self.mute)
        pb=QPushButton('vol+');vl.addWidget(pb);pb.clicked.connect(self.vol_p)
        pb=QPushButton('vol-');vl.addWidget(pb);pb.clicked.connect(self.vol_m)
        self.l=QLabel();vl.addWidget(self.l)
    def play2(self):
        self.player=VideoPlayer('D:/2.mp4')
        self.player.l=self.l

    def play(self):
        self.t1=threading.Thread(target=self.play2)
        self.t1.start()

    def pause(self):self.player.player.toggle_pause()
    def seek_p(self):self.player.seek_p()
    def seek_m(self):self.player.seek_m()
    def mute(self):
        try:
            if (self.player.player.get_volume()>0.0):self.player.player.set_volume(0.0)
            else:self.player.player.set_volume(1.0)
        except:pass
    def vol_p(self):
        self.player.player.set_volume(self.player.player.get_volume() + 0.1)
        print(self.player.player.get_volume())
    def vol_m(self):
        self.player.player.set_volume(self.player.player.get_volume() - 0.1)
        print(self.player.player.get_volume())

    def close(self):
        try:
            self.player.close=True
            time.sleep(1)
        except:pass

    def closeEvent(self, event):
        try:
            self.player.close=True
            time.sleep(1)
        except:pass



if __name__ == '__main__':

    app = QApplication(sys.argv)
    window=ed()
    window.showMaximized()
    sys.exit(app.exec_())