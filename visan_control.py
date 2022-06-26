from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os,sys
from visan_qt import *
import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import psutil


class system():
    def __init__(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
    def get_brightness(self):return sbc.get_brightness()
    def set_brightness(self,x):sbc.set_brightness(x)
    def get_volume(self):return int(self.volume.GetMasterVolumeLevelScalar()*100)
    def set_volume(self,x):self.volume.SetMasterVolumeLevelScalar(x/100,None)
    def get_battery(self): return psutil.sensors_battery()



class controls(QMainWindow):
    def __init__(self,parent=None):
        super().__init__()

        self.control=scrollwindow();self.setCentralWidget(self.control)
        self.CGL=QVBoxLayout(self.control.widget)

        self.CGL2=QGridLayout();self.CGL.addLayout(self.CGL2)

        pb=button(tip='shutdown',icon=stored('shutdown.png'),w=100,h=100);self.CGL2.addWidget(pb,0,0)
        pb=button(tip='Restart',icon=stored('restart.png'),w=100,h=100);self.CGL2.addWidget(pb,0,1)
        pb=button(tip='Bluetooth',icon=stored('bluetooth.png'),function=None,w=100,h=100);self.CGL2.addWidget(pb,0,2)
        pb=button(tip='Wifi',icon=stored('wifi.png'),w=100,h=100);self.CGL2.addWidget(pb,0,3)

        self.gb=gifbutton2(stored('charging.gif'),text='');self.CGL2.addWidget(self.gb,0,4)

        self.CGL2=QGridLayout();self.CGL.addLayout(self.CGL2)
        pb=button(tip='mute',icon=stored('mute.png'),w=50,h=50,function=self.set_mute);self.CGL2.addWidget(pb,0,0)
        self.s1 = QSlider(Qt.Horizontal);self.CGL2.addWidget(self.s1,0,1);self.s1.valueChanged.connect(self.set_volume)
        self.s1.setRange(0, 100)
        pb=button(tip='unmute',icon=stored('unmute.png'),w=50,h=50,function=self.set_max_vol);self.CGL2.addWidget(pb,0,2)
        self.l1=QLabel();self.CGL2.addWidget(self.l1,0,3)

        pb=button(tip='bright',icon=stored('bright0.png'),w=50,h=50);self.CGL2.addWidget(pb,1,0)
        self.s2 = QSlider(Qt.Horizontal);self.CGL2.addWidget(self.s2,1,1);self.s2.valueChanged.connect(self.set_brightness)
        self.s2.setRange(0, 100)
        pb=button(tip='bright',icon=stored('bright1.png'),w=50,h=50);self.CGL2.addWidget(pb,1,2)
        self.l2=QLabel();self.CGL2.addWidget(self.l2,1,3)

        self.ci=system()
        self.set_defaults()
        self.checkbattery()

        timer = QTimer()
        timer.timeout.connect(self.checkbattery)
        timer.setInterval(5000)
        timer.start()

    def checkbattery(self):
        battery=self.ci.get_battery()
        if battery.power_plugged==True:charge='charging : '
        else: charge=''
        self.gb.l.setText(charge+str(battery.percent)+'%')


    def set_defaults(self):
        #self.s2.setValue(self.ci.get_brightness())
        self.s1.setValue(self.ci.get_volume())
    def set_brightness(self):
        self.ci.set_brightness(self.s2.value())
        self.l2.setText(str(self.s2.value())+'%')
    def set_volume(self):
        self.ci.set_volume(self.s1.value())
        self.l1.setText(str(self.s1.value())+'%')
    def set_mute(self):self.ci.set_volume(0);self.s1.setValue(0)
    def set_max_vol(self):self.ci.set_volume(100);self.s1.setValue(100)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window=controls()
    window.showMaximized()
    sys.exit(app.exec_())