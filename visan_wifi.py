from visan_qt import *
import threading
from socket import *

class bluecontrol(QMainWindow):
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
        nearby_devices = discover_devices(lookup_names=True)
        self.LN.setText(str(len(nearby_devices)))
        self.cb.addItems([name+':'+str(bdaddr) for bdaddr,name in nearby_devices])
        for bdaddr,name in nearby_devices:
            print(bdaddr)




    def startb(self):
        self.Sock = socket(AF_INET, SOCK_DGRAM)
    def receiveb(self):pass
    def send(self):
        self.Sock.sendto(bytes(self.LE.text(),'utf-8'), ("192.168.0.168", 13000))
    def startserver(self):
        self.t1=threading.Thread(target=self.startb)
        self.t1.start()
    def closeb(self):
        self.Sock.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window=bluecontrol()
    window.showMaximized()
    sys.exit(app.exec_())