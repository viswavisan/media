from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
import sys,os

def stored(x):
    try:base_path = sys._MEIPASS
    except Exception:base_path = os.path.abspath(".")
    return os.path.join(base_path,'stored/'+x).replace('\\','/')

class QVideoWidget(QVideoWidget):
    def __init__(self):
        super().__init__()
    def mouseDoubleClickEvent(self, event):
        self.setFullScreen(not self.isFullScreen())
        event.accept()

class qmplayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.addtoolbar()
        self.adddock()
        self.video = QVideoWidget()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose);
        self.setCentralWidget(self.video)

        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.player.setVideoOutput(self.video)

        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(r"C:\Users\Kokila\Documents\GitHub\media\sample\3.avi")))
        self.video.show()
        #help(self.player)
        self.player.durationChanged.connect(self.durationChanged)
        self.player.positionChanged.connect(self.positionChanged)
        self.voll.setText('Vol:'+str(self.player.volume()))


    def select_file(self,File=None):
        try:
            print(File)
            if File==None:File=QFileDialog.getOpenFileName(self,'Single File','','Video Files (*.avi)')[0]
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(File)))
            self.player.play()
        except Exception as e:print(e)

    def play(self):self.player.play()
    def stop(self):self.player.stop()
    def pause(self):self.player.pause()
    def set_volume(self,x):
        self.player.setVolume(self.player.volume()+x)

        self.voll.setText('Vol:'+str(self.player.volume()))
    def mute(self):
       self.player.setMuted(not self.player.isMuted())

    def closeEvent(self, event):self.player.stop()

    def setPosition(self,position):
        self.player.setPosition(position)

    def addtoolbar(self):
        ToolBar = self.addToolBar("view")

        b=QAction(QtGui.QIcon(stored('open.png')),"file",self);ToolBar.addAction(b);b.triggered.connect(lambda:self.select_file(File=None))
        b=QAction(QtGui.QIcon(stored('run.png')),"play",self);ToolBar.addAction(b);b.triggered.connect(self.play)
        b=QAction(QtGui.QIcon(stored('stop.png')),"stop",self);ToolBar.addAction(b);b.triggered.connect(self.stop)
        b=QAction(QtGui.QIcon(stored('pause.png')),"pause",self);ToolBar.addAction(b);b.triggered.connect(self.pause)
        b=QAction(QtGui.QIcon(stored('forward.png')),"seek+",self);ToolBar.addAction(b);#b.triggered.connect(self.seek_p)
        b=QAction(QtGui.QIcon(stored('backward.png')),"seek-",self);ToolBar.addAction(b);#b.triggered.connect(self.seek_m)
        b=QAction(QtGui.QIcon(stored('mute.png')),"mute",self);ToolBar.addAction(b);b.triggered.connect(self.mute)
        b=QAction(QtGui.QIcon(stored('plus.png')),"vol+",self);ToolBar.addAction(b);b.triggered.connect(lambda:self.set_volume(1))
        b=QAction(QtGui.QIcon(stored('minus.png')),"vol-",self);ToolBar.addAction(b);b.triggered.connect(lambda:self.set_volume(-1))

        b=QAction(QtGui.QIcon(stored('plus.png')),"zoom+",self);ToolBar.addAction(b);#b.triggered.connect(self.zoomin)
        b=QAction(QtGui.QIcon(stored('minus.png')),"zoom-",self);ToolBar.addAction(b);#b.triggered.connect(self.zoomout)
        b=QAction(QtGui.QIcon(stored('resize.png')),"Full screen",self);ToolBar.addAction(b);b.triggered.connect(self.fullscreen)

    def fullscreen(self):
        try:#self.video.setFullscreen(True)
            self.video.setFullScreen(not self.video.isFullScreen())
        except Exception as e:print(e)

    def adddock(self):
        dockw = QDockWidget("controls", self)
        dockw.setTitleBarWidget(QWidget(None))
        self.addDockWidget(Qt.BottomDockWidgetArea, dockw)
        dw=QWidget();dockw.setWidget(dw)
        VL=QHBoxLayout(dw)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)

        self.positionSlider.sliderMoved.connect(self.setPosition)
        VL.addWidget(self.positionSlider)
        self.tl=QLabel();VL.addWidget(self.tl)
        self.voll=QLabel();VL.addWidget(self.voll)


    def durationChanged(self,duration):
        self.ttime=str(self.player.duration()//60000)+':'+str((self.player.duration()%60000)//1000)
        self.tl.setText('0:0/'+self.ttime)
        self.positionSlider.setRange(0, duration)
    def positionChanged(self,position):
        self.ctime= str(self.player.position()//60000)+':'+str((self.player.position()%60000)//1000)
        self.tl.setText(self.ctime+'/'+self.ttime)
        self.positionSlider.setValue(position)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window=qmplayer()
    window.showMaximized()
    sys.exit(app.exec_())