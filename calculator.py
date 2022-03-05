from math import *
from visan_qt import *

class QTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()

class calc(QWidget):
    def __init__(self):
        super().__init__()
        vl=QVBoxLayout(self)
        self.display=QTextEdit()
        self.display.setAlignment(Qt.AlignRight)
        vl.addWidget(self.display)
        self.display.setMaximumHeight(100)
        #self.display.setReadOnly(True)
        self.display.keyPressEvent = self.keyPressEvent

        hl=QHBoxLayout();vl.addLayout(hl)
        self.answerdisply=QLineEdit()
        hl.addWidget(QLabel('ANS:'))
        hl.addWidget(self.answerdisply)
        self.answerdisply.setReadOnly(True)

        self.gl=QGridLayout()
        vl.addLayout(self.gl)
        self.addbuttons()
        vl.addStretch()
    def addbuttons(self):
        Bs=[
            ['<-','CE','','*'],
            [7,8,9,'+'],
            [4,5,6,'-'],
            [1,2,3,'/'],
            ['00',0,'.','='],
            ['(',')','pi','e'],
            ['sin(','cos(','tan(','degrees('],
            ['asin(','acos(','atan(','radians('],
            ['exp(','log(','ln(','factorial('],
            ['abs(','x²','x³','xⁿ'],
            ['sqrt(','f->e','e->f','ans']]

        for x,r in enumerate(Bs):
            for y,c in enumerate(r):
                self.gl.addWidget(button(function=lambda c=c:self.fun(c),text=str(c),h=50),x,y)
    def custom_format(num, decimals_power_of_ten, digits_after_dot):
        formated = '{:e}'.format(num)
        parts = formated.split('e')
        new_decimal = ''
        new_power = ''
        if decimals_power_of_ten != 0:
            part1 = float(parts[0])*(10**decimals_power_of_ten)
            d = "{:." +str(digits_after_dot)+ "f}"
            new_decimal = d.format(part1)
            new_power_int = int(parts[1][1:]) - decimals_power_of_ten
            if new_power_int > 0 and new_power_int < 9:new_power =  'e+0' + str(new_power_int)
            else:
                if new_power_int > 0:new_power = 'e+'+str(new_power_int)
                else:new_power = 'e'+str(new_power_int)
            formated = new_decimal + new_power
        return formated
    def fun(self,c):
        if c=='x²':c='**2'
        if c=='x³':c='**3'
        if c=='xⁿ':c='**'

        if c=='=':
            x=self.display.toPlainText().split('\n')[-1]
            try:
                if 'ans' in x: x=x.replace('ans',str(self.result))
                self.result=eval(x);self.display.append('='+str(self.result)+'\n')
                self.answerdisply.setText(str(self.result))
            except Exception as e:self.display.append('Invalid');print(e)
        elif c=='CE':
            self.display.clear()
            self.display.setAlignment(Qt.AlignRight)
        elif c=='<-':
            self.display.textCursor().deletePreviousChar()
        elif c=='f->e':
            x=self.display.toPlainText().split('\n')[-1]
            x=x.replace('ans',str(self.result))
            self.display.append("{:e}".format(float(x)))
        elif c=='e->f':
            x=self.display.toPlainText().split('\n')[-1]
            x=x.replace('ans',str(self.result))
            self.display.append("{:.16f}".format(float(x)))


        else:self.display.insertPlainText(str(c))



    def keyPressEvent(self, e):
        if (e.key()  == Qt.Key_Return or e.key()==16777221):self.fun('=')
        elif e.key()  == Qt.Key_Escape:self.fun('CE')
        else:super(QTextEdit, self.display).keyPressEvent(e)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window=calc()
    window.show()
    sys.exit(app.exec_())