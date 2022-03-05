from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import notepad2 as np
import os
import pandas

class Qtable(QTableWidget):
    def __init__(self):
        super().__init__()
        #default
        self.horizontalHeader().setStyleSheet("::section{Background-color:lightgray;border-radius:10px;}")
        self.setStyleSheet("selection-background-color: blue;")
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.mme=None
        self.horizontalHeader().sectionClicked.connect(self.filterwin)
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
        for r in range(self.rowCount()):
            if key in self.item(r,c).text():self.showRow(r)
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

    def getheader(self):
        return [self.horizontalHeaderItem(c).text() for c in range(self.columnCount())]

    def getcolumn(self,c):
        return [self.item(r,c).text()  for r in range(self.rowCount())]
    def getcolumns(self,C):
        return [[self.item(r,c).text()  for c in C] for r in range(self.rowCount())]


def stored(x):
    try:base_path = sys._MEIPASS
    except Exception:base_path = os.path.abspath(".")
    return os.path.join(base_path,'stored/'+x).replace('\\','/')

class pyexcel(QMainWindow):
    def __init__(self,parent=None):
        super().__init__()
        self.menu = self.menuBar()
        self.viewmenu = QMenu("&View", self);self.menu.addMenu(self.viewmenu)
        b=QAction(QtGui.QIcon(stored("Editor.png")),"Editor",self);self.viewmenu.addAction(b);b.triggered.connect(lambda:dock.setVisible(dock.isVisible()==False))

        self.sheets= QTabWidget();self.setCentralWidget(self.sheets)
        self.sheets.setTabPosition(QTabWidget.South)

        self.SE=np.script_editor()
        dock = QDockWidget("pyMacro",self)
        dock.setWidget(self.SE)
        self.addDockWidget(Qt.RightDockWidgetArea,dock)

        ToolBar = self.addToolBar("view")
        b=QAction(QtGui.QIcon(stored("open.png")),"open",self);ToolBar.addAction(b);b.triggered.connect(lambda:self.sheet.openfile())


        self.sbar=self.statusBar()

        self.addsheets()

    def addsheets(self):
        self.sheet=Qtable()
        self.sheets.addTab(self.sheet,'GENERAL')
        self.sheet.setRowCount(10)
        self.sheet.setColumnCount(10)
        #self.table=QTableWidget()


app = QApplication([])
window=pyexcel()
window.showMaximized()
app.exec_()