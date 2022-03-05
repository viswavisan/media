from visan_qt import *
import threading
import serial
import serial.tools.list_ports


class comcontrol(QMainWindow):
    def __init__(self,parent=None):
        super().__init__()

        self.control=scrollwindow();self.setCentralWidget(self.control)
        self.VL=QVBoxLayout(self.control.widget)

        hl=QHBoxLayout();self.VL.addLayout(hl)
        l=QLabel('Devices:');l.setFixedWidth(100)
        hl.addWidget(l)
        self.LN=QLabel('0');hl.addWidget(self.LN)
        self.LN.setFixedWidth(100)
        self.cb=QComboBox();hl.addWidget(self.cb)
        hl.addWidget(button(icon=stored('reload'),w=30,h=30,function=self.getdevices))

        hl=QHBoxLayout();self.VL.addLayout(hl)
        self.bl=QLabel('Disconnected');hl.addWidget(self.bl)
        hl.addWidget(button(text='connect',function=self.startserver))
        hl.addWidget(button(text='stop',function=self.closeb))

        self.bte=QTextEdit()
        self.VL.addWidget(self.bte)

        hl=QHBoxLayout();self.VL.addLayout(hl)
        self.LE=QLineEdit();hl.addWidget(self.LE)
        hl.addWidget(button(icon=stored('send.png'),w=40,h=40,function=self.send))

        #self.getdevices()



    def getdevices(self):
        self.cb.clear()
        ports = serial.tools.list_ports.comports()
        self.Ports={str(port):port for port in ports}
        self.cb.addItems(self.Ports.keys())


    def startb(self):
        try:
            cport=self.Ports[self.cb.currentText()].name
            self.serialPort = serial.Serial(port=cport, baudrate=9600, timeout=0, parity=serial.PARITY_EVEN, stopbits=1)
            self.bl.setText('client accepted')
            self.bc=True
            self.receiveb()
        except Exception as e:print(e)
    def receiveb(self):
        try:
            while self.bc==True:
                data = self.serialPort.readline()
                if data:self.bte.append(data.decode("utf-8"))
        except Exception as e:print(e)
    def send(self):
        self.serialPort.write(self.LE.text().encode("utf-8"))

    def startserver(self):
        self.t1=threading.Thread(target=self.startb)
        self.t1.start()

    def closeb(self):
        self.bc=False
        self.bl.setText('server closed')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window=comcontrol()
    window.showMaximized()
    sys.exit(app.exec_())