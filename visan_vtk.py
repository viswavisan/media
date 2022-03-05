from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os,sys
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk

def stored(x):
    try:base_path = sys._MEIPASS
    except Exception:base_path = os.path.abspath(".")
    return os.path.join(base_path,'stored/'+x).replace('\\','/')

class Q3D(QVTKRenderWindowInteractor):
    def __init__(self):
        super().__init__()
        vtk.vtkObject.GlobalWarningDisplayOff()
        self.Start()
        self.renderer= vtk.vtkRenderer()
        self.render_window=self.GetRenderWindow()
        self.render_window.AddRenderer(self.renderer)
        self.mouse=vtk.vtkInteractorStyleTrackballCamera()
        self.SetInteractorStyle(self.mouse)
        self.renderer.SetBackground(1/255,20/255,40/255)
        self.axis()

    def axis(self):
        self.axesxyz=vtk.vtkOrientationMarkerWidget()
        axes = vtk.vtkAxesActor()
        self.axesxyz.SetOrientationMarker(axes)
        self.axesxyz.SetInteractor(self)
        self.axesxyz.EnabledOn()
        self.axesxyz.InteractiveOff()
    def toggleaxis(self):
        self.axesxyz.SetEnabled(int(self.axesxyz.GetEnabled()==0))
        self.Render()



    def addfile(self,file):
        reader = vtk.vtkSTLReader();reader.SetFileName(file)
        mapper = vtk.vtkPolyDataMapper();mapper.SetInputConnection(reader.GetOutputPort())
        actor = vtk.vtkActor();self.renderer.AddActor(actor);actor.SetMapper(mapper)
        return actor
    def clicked(self,m,event):
        return
        modifiers = QApplication.keyboardModifiers()
        clickPos = m.GetInteractor().GetEventPosition()
        picker =vtk.vtkPropPicker()
        picker.PickProp(clickPos[0], clickPos[1], self.renderer)
        actor=picker.GetActor()
        m.OnLeftButtonDown()
        if actor:return actor
    def sizeHint(self):return QtCore.QSize(500,500)
    def fit(self):self.renderer.ResetCamera();self.Render()

    def loadfolder(self,path):
        try:
            self.clearwindow()
            if not os.path.isdir(path):return
            files=os.listdir(path)
            self.parts={}
            for file in files:
                if not file.endswith('.stl'):continue
                actor=self.addfile(path+'/'+file)
                actor.name=file.replace('.stl','')
                self.parts[actor.name]=actor
            self.fit()
        except Exception as e:print(e)
    def changebg(self):
        print(help(self.renderer))
        color = QColorDialog.getColor()
        if color.isValid():
            (R,G,B,A)=color.getRgb()
            self.renderer.SetBackground(R/255,G/255,B/255)

    def gradiant(self):
        self.renderer.SetGradientBackground(int(self.renderer.GetGradientBackground()==False))
        self.Render()


    def loadfolder2(self):
        folder=QFileDialog.getExistingDirectory()
        self.loadfolder(folder)

    def showonly(self,actors):
        for k,v in self.parts.items():
            if v.name in actors:v.SetVisibility(True)
            else:v.SetVisibility(False)

    def showactor(self,actor):
        self.parts[actor].SetVisibility(True)

    def showactors(self,actors):
        for actor in actors:self.parts[actor].SetVisibility(True)

    def hideactor(self,actor):
        self.parts[actor].SetVisibility(False)
    def hideactors(self,actors):
        for actor in actors:self.parts[actor].SetVisibility(False)

    def selectactor(self,actor):
        actor.GetProperty().SetOpacity(1)
        actor.GetProperty().SetColor(1,0,0)

    def actors_deselect(self):
        for actor in self.parts.values():
            actor.GetProperty().SetOpacity(0.5)
            actor.GetProperty().SetColor(1,1,1)

    def visible_actors(self):return[v for k,v in pid.items() if v.GetVisibility()==1]

    def locate(self,actors):
        try:
            va={k:v for k,v in self.parts.items() if v.GetVisibility()==1}
            self.showonly(actors)
            self.renderer.ResetCamera()
            for k,v in va.items():v.SetVisibility(True)
        except Exception as e:print(e)

    def copy_files2(self,folder2):
        try:
            folder=QFileDialog.getExistingDirectory()
            if folder=='':return
            if os.path.isdir(folder2):shutil.rmtree(folder2)
            os.mkdir(folder2)
            for file in os.listdir(folder):
                shutil.copy2(folder+'/'+file,folder2)
        except Exception as e:print(e)

    def resetcolor(self,file):
        filedata=open(file, 'w', newline='')
        writer = csv.writer(filedata)
        data=[[k,random.randint(0,255)/255,random.randint(0,255)/255,random.randint(0,255)/255]for k,v in self.parts.items()]
        self.partscolor= {line[0]:line[1:] for line in data}
        writer.writerows(data)
        filedata.close()

    def colormode(self,file):
        try:
            if not os.path.isfile(file):self.resetcolor(file)
            filedata=open(file)
            data = csv.reader(filedata)
            self.partscolor=C={line[0]:line[1:] for line in data}
            filedata.close()

            for k,v in self.parts.items():
                if k not in C:v.GetProperty().SetColor(random.randint(0,255)/255,random.randint(0,255)/255,random.randint(0,255)/255)
                else:v.GetProperty().SetColor(float(C[k][0]),float(C[k][1]),float(C[k][2]))
                v.GetProperty().SetOpacity(1)
            self.Render()
        except Exception as e:print(e)

    def clearwindow(self):
        self.renderer.RemoveAllViewProps()

    def saveasimage(self):
        filename=QFileDialog.getSaveFileName(window,"","","png Files (*png)")[0]
        w2if =vtk.vtkWindowToImageFilter()
        w2if.SetInput(self.render_window)
        w2if.Update()
        writer = vtk.vtkPNGWriter()
        writer.SetFileName(filename)
        writer.SetInputData(w2if.GetOutput())
        writer.Write()


class vtkviewer(QMainWindow):
    def __init__(self,parent=None):
        super().__init__()
        self.win3d= Q3D();self.setCentralWidget(self.win3d)

        ToolBar = self.addToolBar("view")
        b=QAction(QtGui.QIcon(stored("axis.png")),"axis",self);ToolBar.addAction(b);b.triggered.connect(self.win3d.toggleaxis)
        b=QAction(QtGui.QIcon(stored("load.png")),"load",self);ToolBar.addAction(b);b.triggered.connect(self.win3d.loadfolder2)
        b=QAction(QtGui.QIcon(stored("color.png")),"bg",self);ToolBar.addAction(b);b.triggered.connect(self.win3d.changebg)
        b=QAction(QtGui.QIcon(stored("gradiant.png")),"gradiant",self);ToolBar.addAction(b);b.triggered.connect(self.win3d.gradiant)
        b=QAction(QtGui.QIcon(stored("save.png")),"save",self);ToolBar.addAction(b);b.triggered.connect(self.win3d.saveasimage)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window=vtkviewer()
    window.showMaximized()
    sys.exit(app.exec_())
