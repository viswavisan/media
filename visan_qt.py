from PyQt5 import QtGui,QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
import os,sys
import pyqtgraph as pg



def stored(x):
    try:base_path = sys._MEIPASS
    except Exception:base_path = os.path.abspath(".")
    return os.path.join(base_path,'stored/'+x).replace('\\','/')

class button(QPushButton):
    def __init__(self,text='',function=None,icon=None,h=None,w=None,flat=False,tip=None,curser=None,arg=[],checkable=False):
        super().__init__()
        self.setText(text)
        self.setFlat(flat)
        self.setCheckable(checkable)
        if w!=None: self.setFixedWidth(w)
        if h!=None: self.setFixedHeight(h)
        if icon!=None:self.setIcon(QtGui.QIcon(icon));self.setFlat(True);self.setIconSize(self.size())
        if curser=='hand':self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        if tip!=None:self.setToolTip('<div style="background-color:white">'+tip+'</div>')
        if function!=None:self.clicked.connect(self.Function)
        self.function=function
        self.arg=arg

    def Function(self,sig):
        try:
            arg=[sig,self]+self.arg
            x=len(arg)-self.function.__code__.co_argcount
            if x>0:arg=arg[x+1:]
            self.function(*arg)
        except Exception as e:print(e)

class scrollwindow(QScrollArea):
    def __init__(self,parent=None,vs=Qt.ScrollBarPolicy.ScrollBarAlwaysOff,hs=Qt.ScrollBarPolicy.ScrollBarAlwaysOff,size=None,bg=None,w=None):
        super().__init__()
        if parent!=None: parent.addWidget(self)
        self.widget = QFrame();self.setWidget(self.widget)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(hs)
        self.setVerticalScrollBarPolicy(vs)
        if size!=None:  self.widget.setFixedHeight(size)
        if w!=None:self.widget.setFixedHeight(size)
        if bg!=None: self.widget.setStyleSheet("background-color:"+bg)

class  gifbutton(QLabel):
    def __init__(self,gif='',function=None,w=200,h=200,arg=None,zsize=None,text=None):
        super().__init__()

        self.movie=QtGui.QMovie(gif)
        self.movie.setScaledSize(QtCore.QSize().scaled(h, w, Qt.KeepAspectRatio))
        self.function=function
        self.arg=arg
        self.setMovie(self.movie)
        self.setMaximumWidth(w)
        self.movie.start();self.movie.stop()
        self.setFixedHeight(h+50)
        if text !=None:
            self.setLayout(QVBoxLayout())
            l2=QLabel(text)
            self.layout().addWidget(l2)
            l2.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignHCenter)

    def enterEvent(self, e):self.movie.start()
    def leaveEvent(self, e):self.movie.stop();self.movie.start();self.movie.stop()
    def mousePressEvent(self, e):
        if self.function==None:return
        if self.arg!=None:self.function(self.arg)
        else:self.function()

class  gifbutton2(QLabel):
    def __init__(self,gif='',function=None,w=200,h=200,arg=None,zsize=None,text=None):
        super().__init__()

        self.movie=QtGui.QMovie(gif)
        self.movie.setScaledSize(QtCore.QSize().scaled(h, w, Qt.KeepAspectRatio))
        self.function=function
        self.arg=arg
        self.setMovie(self.movie)
        self.setMaximumWidth(w)
        self.movie.start()
        self.setFixedHeight(h+50)
        if text !=None:
            self.setLayout(QVBoxLayout())
            self.l=QLabel(text)
            self.layout().addWidget(self.l)
            self.l.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignHCenter)



class Browser(QMainWindow):
    def __init__(self,parent=None):
        super().__init__()
        if parent!=None:parent.addWidget(self)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('http://google.com'))
        self.setCentralWidget(self.browser)

        ToolBar=self.addToolBar("view")
        b=QAction(QtGui.QIcon(stored('previous.png')),"Prev",self);ToolBar.addAction(b);b.triggered.connect(self.browser.back)
        b=QAction(QtGui.QIcon(stored('next.png')),"Next",self);ToolBar.addAction(b);b.triggered.connect(self.browser.forward)
        b=QAction(QtGui.QIcon(stored('reload.png')),"Refresh",self);ToolBar.addAction(b);b.triggered.connect(self.browser.reload)
        b=QAction(QtGui.QIcon(stored('home.png')),"Home",self);ToolBar.addAction(b);b.triggered.connect(self.home)

        self.searchBar = QLineEdit();self.searchBar.returnPressed.connect(self.loadUrl)
        ToolBar.addWidget(self.searchBar)
        self.browser.urlChanged.connect(self.updateUrl)
    def home(self):self.browser.setUrl(QUrl('http://google.com'))
    def loadUrl(self):self.browser.setUrl(QUrl(self.searchBar.text()))
    def updateUrl(self, url):
        if url.toString()=='about:blank':
            glink='https://www.google.com/search?q='+self.searchBar.text()
            self.browser.setUrl(QUrl(glink))
            self.searchBar.setText(glink)
        else:self.searchBar.setText(url.toString())


class QLineNumberArea(QWidget):
    def __init__(self, editor):super().__init__(editor);self.codeEditor = editor
    def sizeHint(self):return QSize(self.editor.lineNumberAreaWidth(), 0)
    def paintEvent(self, event):self.codeEditor.lineNumberAreaPaintEvent(event)

class QCodeEditor(QPlainTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.info_win=None
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.updateLineNumberAreaWidth(0)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.keywords=['False', 'None', 'True', 'and', 'as', 'assert', 'async','await', 'break', 'class', 'continue', 'def', 'del', 'elif',
'else', 'except', 'finally', 'for', 'from', 'global','if', 'import', 'in', 'is', 'lambda','nonlocal', 'not', 'or', 'pass', 'raise',
'return', 'try', 'while', 'with', 'yield']

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:max_value /= 10;digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:self.lineNumberArea.scroll(0, dy)
        else:self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))


    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)
        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignRight, number)
            block = block.next();top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def keyPressEvent(self, event):
        tc=self.textCursor();self.setTextCursor(tc);charf=tc.charFormat()
        #intent
        if event.key()==Qt.Key_Return:
            try:
                intent=''
                tc.select(tc.LineUnderCursor)
                for x in tc.selectedText():
                    if x not in ['','\t']:break
                    intent+=x
                if str(tc.selectedText()).endswith(':'):intent=intent+'    '
                super(QCodeEditor, self).keyPressEvent(event)
                self.insertPlainText(intent)
            except Exception as e:print(e)
            return
        #color key
        else:
            try:
                super(QCodeEditor, self).keyPressEvent(event)
                tc.select(tc.WordUnderCursor)
                if tc.selectedText() in self.keywords:charf.setForeground(QtGui.QColor(255, 0, 0));tc.setCharFormat(charf)
                else:charf.setForeground(QtGui.QColor(0, 0, 0));tc.setCharFormat(charf)
            except Exception as e:print(e)

    def highlightCurrentLine(self):
        try:
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(QtGui.QColor(Qt.yellow).lighter(160))
            selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            self.setExtraSelections([selection])
        except Exception as e:print(e)

    def gotoLine(self):
        try:
            n, ok = QInputDialog.getInt(self, 'input dialog', 'Enter Line number')
            if n < 1:self.printx("The number must be greater than 1");return
            doc = self.document()
            self.setFocus()
            if n > doc.blockCount():self.insertPlainText("\n" * (n - doc.blockCount()))
            cursor = QTextCursor(doc.findBlockByLineNumber(n - 1))
            self.setTextCursor(cursor)
        except Exception as e:print(e)

    def Find(self,text):
        if text=='':return
        try:
            col =QtGui.QColor(0, 0, 255)
            fmt = QTextCharFormat()
            fmt.setForeground(col)
            self.moveCursor(QTextCursor.Start)
            countWords = 0
            while self.find(text, QTextDocument.FindWholeWords):      # Find whole words
                self.mergeFormatOnWordOrSelection(fmt)
                countWords += 1
            self.printx('count:'+str(countWords))
        except Exception as e:print(e)

    def mergeFormatOnWordOrSelection(self,format):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(format)
        self.mergeCurrentCharFormat(format)

    def replace(self,old,new):
        try:
            self.textCursor().beginEditBlock()
            doc = self.document()
            cursor = QtGui.QTextCursor(doc)
            while True:
                cursor = doc.Find(old)
                if cursor.isNull():break
                cursor.insertText(new)
            self.textCursor().endEditBlock()
        except Exception as e:print(e)

    def printx(self,x):
        if self.info_win!=None:self.info_win.appendPlainText(x)
        print(x)

    def run(self):
        try:exec(self.toPlainText());self.printx('script run completed')
        except Exception as e:self.printx(str(e))
    def openpy(self):
        try:
            f=QFileDialog.getOpenFileName(self,'Single File','python','*.py')[0]
            self.appendPlainText(open(f,'r').read())
        except Exception as e:print(str(e))
        try:
            for text in self.keywords:self.Find(text)
        except Exception as e:print(str(e))

    def savepy(self):
        try:
            filename=QFileDialog.getSaveFileName(None, 'Save File','',"Python Files (*.py)")
            f=open(filename[0],'w');f.write(script_win.toPlainText());f.close()
        except Exception as e:self.printx.appendPlainText(str(e))

class script_editor(QMainWindow):
    def __init__(self,parent=None):
        super().__init__()
        self.page=QCodeEditor();self.setCentralWidget(self.page)

        ToolBar = self.addToolBar("view")
        b=QAction(QtGui.QIcon(stored("goto.png")),"goto",self);ToolBar.addAction(b);b.triggered.connect(lambda:self.page.gotoLine())
        b=QAction(QtGui.QIcon(stored("find.png")),"find",self);ToolBar.addAction(b);b.triggered.connect(lambda:self.page.Find())
        b=QAction(QtGui.QIcon(stored("replace.png")),"replace",self);ToolBar.addAction(b);b.triggered.connect(lambda:self.page.replace())
        b=QAction(QtGui.QIcon(stored("open.png")),"open",self);ToolBar.addAction(b);b.triggered.connect(lambda:self.page.openpy())
        b=QAction(QtGui.QIcon(stored("run.png")),"run",self);ToolBar.addAction(b);b.triggered.connect(lambda:self.page.run())
        b=QAction(QtGui.QIcon(stored("save.png")),"save",self);ToolBar.addAction(b);b.triggered.connect(lambda:self.page.savepy())


class Qtable(QTableWidget):
    def __init__(self):
        super().__init__()
        #default
        self.horizontalHeader().setStyleSheet("::section{Background-color:lightgray;border-radius:10px;}")
        self.setStyleSheet("selection-background-color: blue;")
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.mme=None
        self.horizontalHeader().sectionClicked.connect(self.filterwin)
        self.customContextMenuRequested.connect(self.rightclick_menu)
    def openfile(self):
        file=QFileDialog.getOpenFileName(self,'Single File','','*.csv')[0]
        self.df=pandas.read_csv(file,keep_default_na=False,header=None)
        self.datalist=self.df.values.tolist()
        self.set_data(self.datalist)
    def set_data(self,data):
        self.setUpdatesEnabled(False)
        self.setRowCount(len(data))
        def checkset(r,c):
            try:return str(data[r][c])
            except: return ''
        [self.setItem(r,c,QTableWidgetItem(checkset(r,c)))  for c in range(self.columnCount()) for r in range(len(data))]
        self.setUpdatesEnabled(True)
    def set_header(self,header):
        self.setColumnCount(len(header));self.setHorizontalHeaderLabels(header)
    def sort(self,col):self.sortItems(col, QtCore.Qt.AscendingOrder)

    def insert_data(self,data):
        self.insertRow(self.rowCount())
        for i,x in enumerate(data):self.setItem(self.rowCount()-1,i,QTableWidgetItem(str(x)))
        return

    def search(self,key,columns=None):
        matches = self.findItems(key, Qt.MatchContains)
        res=[]
        for match in matches :
            if columns!=None and match.column() not in columns:continue
            res.append(match)
        return res
    def filter(self,key,c=0):
        self.setUpdatesEnabled(False)
        if key=='':self.clear_filter()
        else:
            for r in range(self.rowCount()):
                if self.item(r,c) is not None and key in self.item(r,c).text():self.showRow(r)
                else:self.hideRow(r)
        self.setUpdatesEnabled(True)
    def hideincolumn(self,key,c=0):
        hidden=[]
        self.setUpdatesEnabled(False)
        for r in range(self.rowCount()):
            if key in self.item(r,c).text():self.hideRow(r);hidden.append(r)
        self.setUpdatesEnabled(True)
        return hidden

    def showincolumn(self,key,c=0):
        shown=[]
        self.setUpdatesEnabled(False)
        for r in range(self.rowCount()):
            if key in self.item(r,c).text():self.showRow(r);shown.append(r)
        self.setUpdatesEnabled(True)
        return(shown)

    def selectincolumn(self,key,c=0):
        hidden=[]
        self.setUpdatesEnabled(False)
        for r in range(self.rowCount()):
            if key in self.item(r,c).text():self.hideRow(r);hidden.append(r)
        self.setUpdatesEnabled(True)
        return hidden

    def unselectincolumn(self,key,c=0):
        shown=[]
        self.setUpdatesEnabled(False)
        for r in range(self.rowCount()):
            if key in self.item(r,c).text():self.showRow(r);shown.append(r)
        self.setUpdatesEnabled(True)
        return(shown)

    def findselect(self,key,columns=None,select=0):
        try:
            matches = self.findItems(key, Qt.MatchContains)
            self.selectRow(matches[0].row())
            self.clearSelection()
            for match in matches :
                if columns!=None and match.column() not in columns:continue
                self.item(match.row(), select).setSelected(True)
        except Exception as e:print(e)
    def filterwin(self,index):
        try:
            menu=QMenu();GL=QGridLayout(menu)
            LE=QLineEdit()
            PB=QPushButton();PB.setIcon(QIcon(stored('filter.png')));PB.clicked.connect(lambda x,LE=LE,c=index:self.filter(LE.text(),c))
            GL.addWidget(PB,0,0)
            GL.addWidget(LE,0,1)
            menu.exec(QtGui.QCursor.pos())
        except Exception as e:print(e)

    def clear_filter(self):
        self.setUpdatesEnabled(False)
        for r in range(self.rowCount()):self.showRow(r)
        self.setUpdatesEnabled(True)

    def mouseMoveEvent(self, event):
        try:
            if self.mme==None:return
            else:self.mme(event)
        except Exception as e:print(e)
    def colfit(self):
        self.resizeColumnsToContents()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

    def selected_rows(self):
        return list(set([cell.row() for cell in self.selectedIndexes()]))

    def getdata(self):
        return [[self.item(r,c).text() if self.item(r,c) is not None else '' for c in range(self.columnCount()) ]  for r in range (self.rowCount())]

    def savedata(self):
        filename=QFileDialog.getSaveFileName(None, 'Save File','',"CSV Files (*.csv)")
        filedata=open(filename[0], 'w', newline='')
        writer = csv.writer(filedata)
        writer.writerows(self.getdata())
        filedata.close()
    def getheader(self):
        return [self.horizontalHeaderItem(c).text() for c in range(self.columnCount())]

    def getcolumn(self,c):
        return [self.item(r,c).text()  for r in range(self.rowCount())]
    def getcolumns(self,C):
        return [[self.item(r,c).text()  for c in C] for r in range(self.rowCount())]

    def rightclick_menu(self):
        try:
            menu=QMenu();GL=QGridLayout(menu)
            PB=QPushButton('Insert Row Above');PB.setIcon(QIcon(stored('insert.png')));PB.clicked.connect(lambda :self.insertRow(self.currentRow()));GL.addWidget(PB,0,0)
            PB=QPushButton('Insert Row Below');PB.setIcon(QIcon(stored('insert.png')));PB.clicked.connect(lambda :self.insertRow(self.currentRow()+1));GL.addWidget(PB,1,0)
            PB=QPushButton('Insert Column Left');PB.setIcon(QIcon(stored('insert.png')));PB.clicked.connect(lambda :self.insertColumn(self.currentColumn()));GL.addWidget(PB,2,0)
            PB=QPushButton('Insert Column Right');PB.setIcon(QIcon(stored('insert.png')));PB.clicked.connect(lambda :self.insertColumn(self.currentColumn()+1));GL.addWidget(PB,3,0)
            PB=QPushButton('Delete Row');PB.setIcon(QIcon(stored('wrong.png')));PB.clicked.connect(lambda :self.removeRow(self.currentRow()));GL.addWidget(PB,4,0)
            PB=QPushButton('Delete Column');PB.setIcon(QIcon(stored('wrong.png')));PB.clicked.connect(lambda :self.removeColumn(self.currentColumn()));GL.addWidget(PB,5,0)
            menu.exec(QtGui.QCursor.pos())
        except Exception as e:print(e)

    def resizecount(self):
        for r in range(self.rowCount()-1,-1,-1):
            data=[self.item(r,c).text() if self.item(r,c) is not None else '' for c in range(self.columnCount())]
            if [i for i in data if i!='']==[]:self.removeRow(r)
            else:break

        for c in range(self.columnCount()-1,-1,-1):
            data=[self.item(r,c).text() if self.item(r,c) is not None else '' for r in range(self.rowCount())]
            if [i for i in data if i!='']==[]:self.removeColumn(c)
            else:break
    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_C and (event.modifiers() & Qt.ControlModifier):
            self.copied_cells = sorted(self.selectedIndexes())
        elif event.key() == Qt.Key_V and (event.modifiers() & Qt.ControlModifier):
            r = self.currentRow() - self.copied_cells[0].row()
            c = self.currentColumn() - self.copied_cells[0].column()
            for cell in self.copied_cells:
                self.setItem(cell.row() + r, cell.column() + c, QTableWidgetItem(cell.data()))


class pycsv(QMainWindow):
    def __init__(self,parent=None):
        super().__init__()
        self.menu = self.menuBar()
        self.filemenu = QMenu("&File", self);self.menu.addMenu(self.filemenu)
        b=QAction(QtGui.QIcon(stored("new.png")),"new",self);self.filemenu.addAction(b);b.triggered.connect(lambda:self.new())

        self.viewmenu = QMenu("&View", self);self.menu.addMenu(self.viewmenu)
        b=QAction(QtGui.QIcon(stored("Editor.png")),"Editor",self);self.viewmenu.addAction(b);b.triggered.connect(lambda:dock.setVisible(dock.isVisible()==False))

        self.sheets= QTabWidget();self.setCentralWidget(self.sheets)
        self.sheets.setTabPosition(QTabWidget.South)

        self.SE=script_editor()
        dock = QDockWidget("pyMacro",self)
        dock.setWidget(self.SE)
        self.addDockWidget(Qt.RightDockWidgetArea,dock)

        ToolBar = self.addToolBar("view")
        b=QAction(QtGui.QIcon(stored("open.png")),"open",self);ToolBar.addAction(b);b.triggered.connect(lambda:self.sheet.openfile())
        b=QAction(QtGui.QIcon(stored("save.png")),"save",self);ToolBar.addAction(b);b.triggered.connect(lambda:self.sheet.savedata())
        b=QAction(QtGui.QIcon(stored("resize.png")),"resize",self);ToolBar.addAction(b);b.triggered.connect(lambda:self.sheet.resizecount())

        self.sbar=self.statusBar()

        self.addsheets()

    def addsheets(self):
        self.sheet=Qtable()
        self.sheets.addTab(self.sheet,'GENERAL')
        self.new()

    def new(self):
        self.sheet.setRowCount(0)
        self.sheet.setColumnCount(0)
        self.sheet.setRowCount(10)
        self.sheet.setColumnCount(10)
        #self.table=QTableWidget()


class qtchart(QWidget):
    def __init__(self):
        super().__init__()
        self.VL=QVBoxLayout(self)

        self.HL=QHBoxLayout();self.VL.addLayout(self.HL)

        self.qtable=Qtable(); self.HL.addWidget(self.qtable)
        self.qtable.set_header(['Time','Value'])
        self.qtable.colfit()

        self.qtable.setFixedWidth(self.qtable.horizontalHeader().length()+19)
        self.qtable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.qtable.verticalHeader().hide()
        self.qtable.cellClicked.connect(self.table_lclick)


        self.plot=pg.PlotWidget();self.HL.addWidget(self.plot)

        self.plot.setBackground('w')
        self.line=self.plot.plot(pen=pg.mkPen('b', width=2),symbolBrush=0, hoverable=True)
        #self.line = PlotCurveItem(pen=pg.mkPen('b', width=2));self.plot.addItem(self.line)
        #self.line =pg.ScatterPlotItem(size=10, brush=pg.mkBrush(30, 255, 35, 255), hoverable=True);self.plot.addItem(self.line)
        self.plot.setLabel('left', 'Vertical Values', units='y')
        self.plot.setLabel('bottom', 'Horizontal Values', units='s')

    def setdata(self,x,y):
        self.qtable.set_data(list(map(list, zip(*[x,y]))))
        self.x=x;self.y=y
        self.update()

    def update(self):self.line.setData(self.x,self.y)

    def table_lclick(self,r,c):
        try:
            def entered():
                try:
                    self.qtable.item(r,c).setText(le.text())
                    if c==0:self.x[r]=float(le.text())
                    elif c==1:self.y[r]=float(le.text())
                    self.update()
                    menu.close()

                except Exception as e:print(e)
            menu=QMenu();vl=QVBoxLayout(menu)
            le=QLineEdit();vl.addWidget(le);le.returnPressed.connect(entered)
            menu.exec_(QCursor.pos())
        except Exception as e:print(e)
    def sizeHint(self):return QtCore.QSize(500,300)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window=pycsv()
    window.showMaximized()
    sys.exit(app.exec_())