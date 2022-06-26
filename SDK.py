from PyQt5 import QtGui,QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import os,sys
from visan_qt import *
from visan_vtk import *
from visan_control import *
from calculator import calc
#from visan_bluz import *
from visan_com import *
import media
import player2
import Image_viewer


class SDK(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stack=QStackedWidget()
        self.setCentralWidget(self.stack)
        ToolBar=QToolBar("Home");self.addToolBar(QtCore.Qt.BottomToolBarArea, ToolBar)
        b=QAction(QtGui.QIcon(stored('python.png')),"Home",self);ToolBar.addAction(b);b.triggered.connect(lambda:self.stack.setCurrentWidget(self.home))
        self.homepage()
        self.addapps()
        self.settingpage()
        self.browser()
        self.calender()
        self.calculator()
        self.Control()
        self.camera()
        self.Editor()
        self.pyexcel()
        self.q3d()
        #self.bluetooth()
        self.com()
        self.vplayer()
        self.ImageViewer()
    def ImageViewer(self):
        self.imview=Image_viewer.QImageViewer()
        self.stack.addWidget(self.imview)
    def com(self):
        self.Com=comcontrol()
        self.stack.addWidget(self.Com)
    def bluetooth(self):
        try:
            self.bluz=bluecontrol()
            self.stack.addWidget(self.bluz)
        except Exception as e:print(e)
    def homepage(self):
        self.home=scrollwindow(self.stack)
        self.HGL=QGridLayout(self.home.widget)
        self.home.widget.setObjectName("bg")
    def pyexcel(self):
        try:
            self.pyexcel=pycsv()
            self.stack.addWidget(self.pyexcel)
        except Exception as e:print(e)

    def browser(self):
        try:
            self.browser=Browser(self.stack)
            self.browser.setObjectName("bg")
        except Exception as e:print(e)
    def calender(self):
        try:
            self.calender=QCalendarWidget()
            self.stack.addWidget(self.calender)
        except Exception as e:print(e)
    def calculator(self):
        try:
            self.calculator=calc()
            self.stack.addWidget(self.calculator)
        except Exception as e:print(e)
    def camera(self):
        try:
            self.camera=media.image_editor()
            self.camera.app=app
            self.stack.addWidget(self.camera)
        except Exception as e:print(e)
    def Editor(self):
        try:
            self.editor=script_editor()
            self.stack.addWidget(self.editor)
        except Exception as e:print(e)

    def Control(self):
        try:
            self.control=controls()
            self.control.control.widget.setObjectName("bg")
            self.stack.addWidget(self.control)
        except Exception as e:print(e)
    def settingpage(self):
        self.setting=scrollwindow(self.stack)
        self.SGL=QGridLayout(self.setting.widget)
        self.SGL.addWidget(QLabel('number of columns'),0,0,Qt.AlignRight)
        LE=QLineEdit();self.SGL.addWidget(LE,0,1);LE.textChanged.connect(lambda:self.arrange(LE))
        LE.setFixedWidth(50)

        self.SGL.addWidget(QLabel('Background image'),1,0)
        b=QPushButton(clicked=self.background);self.SGL.addWidget(b,1,1,Qt.AlignRight)
        b.setFixedWidth(50)

        self.SGL.setRowStretch(self.SGL.rowCount(), 1)
        self.SGL.setColumnStretch(self.SGL.columnCount(), 1)
        self.setting.widget.setObjectName("bg")

    def q3d(self):
        self.q3d=vtkviewer()
        self.stack.addWidget(self.q3d)
    def vplayer(self):
        self.ffplayer=player2.ed()
        self.stack.addWidget(self.ffplayer)
    def arrange(self,LE):
        try:
            try:C=int(LE.text())
            except:return
            r=0;c=0
            size=150
            buttons=self.home.findChildren(gifbutton)
            for b in buttons:
                self.HGL.addWidget(b,r,c)
                c+=1
                if c==C:r+=1;c=0
        except Exception as e:print(e)


    def addapps(self):
        buttons=[['camera.gif',lambda:self.stack.setCurrentWidget(self.camera),'camera'],
                ['calculator.gif',lambda:self.stack.setCurrentWidget(self.calculator),'calculator'],
                ['calender.gif',lambda:self.stack.setCurrentWidget(self.calender),'calender'],
                ['excel.gif',lambda:self.stack.setCurrentWidget(self.pyexcel),'Excel'],
                ['alexa.gif',lambda:self.stack.setCurrentWidget(self.camera),'Assistance'],
                ['voice.gif',lambda:self.stack.setCurrentWidget(self.camera),'Voice-Record'],
                ['setting3.gif',lambda:self.stack.setCurrentWidget(self.setting),'Setting'],
                ['script.gif',lambda:self.stack.setCurrentWidget(self.editor),'Script Editor'],
                ['vtk.gif',lambda:self.stack.setCurrentWidget(self.q3d),'3D Viewer'],
                ['screen.gif',lambda:self.stack.setCurrentWidget(self.camera),'Screen-Record'],
                ['control.gif',lambda:self.stack.setCurrentWidget(self.control),'System-Control'],
                ['browser.gif',lambda:self.stack.setCurrentWidget(self.browser),'Browser'],
                #['bluetooth.gif',lambda:self.stack.setCurrentWidget(self.bluz),'Bluetooth'],
                ['com.gif',lambda:self.stack.setCurrentWidget(self.Com),'Serial Monitor'],
                ['video_player1.gif',lambda:self.stack.setCurrentWidget(self.ffplayer),'FF player'],
                ['QM_video_player.gif',lambda:self.stack.setCurrentWidget(self.player),'Qmedia player'],
                ['gallery.gif',lambda:self.stack.setCurrentWidget(self.imview),'image viewer']]
        C=5
        r=0;c=0
        size=150
        for b in buttons:
            B=gifbutton(stored(b[0]),b[1],w=size,h=size,text=b[2]);self.HGL.addWidget(B,r,c)
            c+=1
            if c==C:r+=1;c=0
    def background(self):
        file=QFileDialog.getOpenFileName(self,'Single File','','')[0]
        stylesheet2='#bg{border-image: url("'+file+'") 0 0 0 0 stretch stretch;}'
        app.setStyleSheet(stylesheet2)


    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.RightButton:
            print("Right Button Clicked")
            menu=QMenu()
            l=QLabel('options')

            vl=QVBoxLayout(menu)
            vl.addWidget(l)
            menu.exec_(QCursor.pos())


stylesheet2='#bg {border-image: url("'+stored('bg.jpg')+'") 0 0 0 0 stretch stretch;}'
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window=SDK()
    app.setStyleSheet(stylesheet2)
    window.showMaximized()
    sys.exit(app.exec_())