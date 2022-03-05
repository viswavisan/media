from visan_qt import *
import threading
from bluetooth import *

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

        server_sock = BluetoothSocket( RFCOMM )
        server_sock.bind(("",PORT_ANY))
        server_sock.listen(1)
        self.server=server_sock

        port = server_sock.getsockname()[1]
        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        advertise_service( server_sock, "TestServer",service_id = uuid,service_classes = [ uuid, SERIAL_PORT_CLASS ],profiles = [ SERIAL_PORT_PROFILE ])
        self.bl.setText('server started')
        self.client, client_info = server_sock.accept()
        server_sock.listen(1)
        print(help(self.client.getpeername()))
        self.bl.setText('client accepted'+str(client_info))
        self.bc=True
        self.receiveb()

    def receiveb(self):
        try:
            while self.bc==True:
                req = self.client.recv(1024)
                self.bte.append(req.decode("utf-8"))
                print(req)
        except Exception as e:print(e)
    def send(self):
        self.client.send(self.LE.text())

    def startserver(self):
        self.t1=threading.Thread(target=self.startb)
        self.t1.start()

    def closeb(self):
        self.bc=False
        self.closeb2()
    def closeb2(self):
        try:self.client.close()
        except:pass
        try:server_sock.close()
        except:pass
        self.bl.setText('server closed')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window=bluecontrol()
    window.showMaximized()
    sys.exit(app.exec_())