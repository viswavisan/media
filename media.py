from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import os
import csv
import wave
import threading

import numpy as np
import cv2
import imutils
import pickle
#pip install cmake
import face_recognition
import imutils.paths as paths

import pyautogui
#pip install pipwin
#pipwin install PyAudio
import pyaudio
from win32api import GetSystemMetrics

import people_also_ask
import pyttsx3

#pip install SpeechRecognition
import speech_recognition as SRG
import time
store = SRG.Recognizer()
engine = pyttsx3.init()
class image_editor(QMainWindow):
    def __init__(self,parent=None):
        super().__init__()

        self.sw=QScrollArea(self)
        self.sw.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.sw.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.l=QLabel()
        self.sw.setWidget(self.l)
        self.setCentralWidget(self.sw)

        ToolBar = self.addToolBar("view")

        b=QAction(QtGui.QIcon(stored('crop.png')),"crop",self);ToolBar.addAction(b);b.triggered.connect(self.crop)
        b=QAction(QtGui.QIcon(stored('save.png')),"save",self);ToolBar.addAction(b);b.triggered.connect(self.save)
        b=QAction(QtGui.QIcon(stored('recenter.png')),"fit",self);ToolBar.addAction(b);b.triggered.connect(self.fit)
        b=QAction(QtGui.QIcon(stored('load.png')),"Load",self);ToolBar.addAction(b);b.triggered.connect(self.select_folder)
        b=QAction(QtGui.QIcon(stored('previous.png')),"previous",self);ToolBar.addAction(b);b.triggered.connect(self.previous)
        b=QAction(QtGui.QIcon(stored('next.png')),"next",self);ToolBar.addAction(b);b.triggered.connect(self.next)
        b=QAction(QtGui.QIcon(stored('bin.png')),"delete",self);ToolBar.addAction(b);b.triggered.connect(self.delete)
        b=QAction(QtGui.QIcon(stored('brush.png')),"draw",self);ToolBar.addAction(b);b.triggered.connect(self.draw)
        b=QAction(QtGui.QIcon(stored('clear.png')),"clear screen",self);ToolBar.addAction(b);b.triggered.connect(self.clear)


        ToolBar = self.addToolBar("Screen-Record")
        b=QAction(QtGui.QIcon(stored('screenshot.png')),"screenshot",self);ToolBar.addAction(b);b.triggered.connect(self.snap)
        b=QAction(QtGui.QIcon(stored('record.png')),"record",self);ToolBar.addAction(b);b.triggered.connect(self.record)
        b=QAction(QtGui.QIcon(stored('stop.png')),"stop",self);ToolBar.addAction(b);b.triggered.connect(self.stoprecord)
        b=QAction(QtGui.QIcon(stored('pause.png')),"pause",self);ToolBar.addAction(b);b.triggered.connect(self.pauserecord)

        ToolBar = self.addToolBar("Camera")
        b=QAction(QtGui.QIcon(stored('camera.png')),"camera",self);ToolBar.addAction(b);b.triggered.connect(self.capture)
        b=QAction(QtGui.QIcon(stored('screenshot.png')),"capture",self);ToolBar.addAction(b);b.triggered.connect(self.saveframe)
        b=QAction(QtGui.QIcon(stored('stop.png')),"stop",self);ToolBar.addAction(b);b.triggered.connect(self.closecam)
        b=QAction(QtGui.QIcon(stored('flip.png')),"flip",self);ToolBar.addAction(b);b.triggered.connect(self.flipcam)

        ToolBar = self.addToolBar("Recorder")
        b=QAction(QtGui.QIcon(stored('vcamera.png')),"video capture",self);ToolBar.addAction(b);b.triggered.connect(self.vcapture)
        b=QAction(QtGui.QIcon(stored('voice.png')),"record",self);ToolBar.addAction(b);b.triggered.connect(self.vrecord)
        b=QAction(QtGui.QIcon(stored('stop.png')),"stop",self);ToolBar.addAction(b);b.triggered.connect(self.vstop)
        b=QAction(QtGui.QIcon(stored('stt.png')),"toText",self);ToolBar.addAction(b);b.triggered.connect(self.stt)
        b=QAction(QtGui.QIcon(stored('ask.png')),"assistance",self);ToolBar.addAction(b);b.triggered.connect(self.assistance)


        dock1 = QDockWidget("Details", self)
        self.TE=QTextEdit()
        dock1.setWidget(self.TE)
        self.addDockWidget(Qt.RightDockWidgetArea,dock1)

        self.sbar=self.statusBar()

        self.getcomment()

        self.currentQRubberBand = QRubberBand(QRubberBand.Rectangle, self)


        dock2 = QDockWidget("Info", self)
        self.infowin=QTextEdit()
        dock2.setWidget(self.infowin)
        self.addDockWidget(Qt.RightDockWidgetArea,dock2)

    def assistance2(self):
        try:

            with SRG.Microphone() as s:
                engine.say('Hi, how can i help you today?');engine.runAndWait()
                audio_input = store.record(s, duration=5)
                try:
                    text=store.recognize_google(audio_input)
                    self.infowin.append(text)

                    x=people_also_ask.get_answer(text)
                    if x['has_answer']==True and x['response']!='':
                        answer=x['response']
                        self.infowin.append(answer)


                    elif x['related_questions']!=[]:
                        answer=people_also_ask.get_simple_answer(x['related_questions'][0].split(':')[-1])
                        self.infowin.append(answer)
                    else:
                        answer="i coudn't able to find answer"

                    def speak():engine.say(answer);engine.runAndWait()
                    self.t1=threading.Thread(target=speak)
                    self.t1.start()


                except Exception as e:self.infowin.append(str(e))
        except Exception as e:print(e)


    def assistance(self):
        self.infowin.append('ask your question...')
        QtCore.QTimer.singleShot(500, self.assistance2)


    def stt2(self):
        with SRG.Microphone() as s:
            audio_input = store.record(s, duration=7)
            try:
                text=store.recognize_google(audio_input)
                self.infowin.append(text)
            except:self.infowin.append("Couldn't process the audio input.")

    def stt(self):
        self.infowin.append('start speek...')
        QtCore.QTimer.singleShot(500, self.stt2)

    def capture(self):
        self.t1=threading.Thread(target=self.capture2)
        self.t1.start()

    def capture2(self):
        try:
            self.flip=False
            self.camstate='start'
            self.cap = cv2.VideoCapture(0)
            while True:
                ret, frame = self.cap.read()
                if self.flip==True:frame = cv2.flip(frame, 90)
                if ret:
                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgbImage.shape
                    Image = QImage(rgbImage.data, w, h, ch * w, QImage.Format_RGB888)
                    self.pixmap=QPixmap.fromImage(Image)
                    self.Show2()
                    if self.camstate=='capture':self.cap.release();break

        except Exception as e:print(e)
    def flipcam(self):
        self.flip= self.flip==False

    def saveframe(self):
        self.camstate='capture'
        filename=QFileDialog.getSaveFileName(self, 'Save File','', 'PNG (*.png)')[0]
        if filename!='':cv2.imwrite(filename, frame)
    def closecam(self):self.camstate='capture'

    def clear(self):
        try:
            self.pixmap=''
            self.l.clear()
        except Exception as e:print(e)


    def closeEvent(self, event):
        try:self.cap.release()
        except:pass

    def vcapture(self):
        try:
            filename=filename=QFileDialog.getSaveFileName(self, 'Save File','', 'MP4 (*.mp4)')[0]
            if filename=='':return
            output = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640,480))

            self.infowin.append('Press D to capture')
            capture = cv2.VideoCapture(0)
            while True:
                isTrue,frame = capture.read()
                cv2.imshow('camera',frame)
                if cv2.waitKey(20) & 0xFF==ord('d'):break
                elif cv2.waitKey(20) & 0xFF==ord('p'):continue
                output.write(frame)

            capture.release()
            output.release()
            cv2.destroyAllWindows()
        except Exception as e:print(e)


    def vrecordstart(self):
        try:
            self.infowin.append('Recording Started')
            self.vrecording=True
            self.p = pyaudio.PyAudio()
            self.stream = self.p.open(format=pyaudio.paInt16,channels=2,rate=44100,frames_per_buffer=1024,input=True)
            self.vframes=[]
            while self.vrecording==True:self.vframes.append(self.stream.read(1024) )
        except Exception as e:print(e)

    def vrecord(self):
        self.t1=threading.Thread(target=self.vrecordstart)
        self.t1.start()

    def vpause(self):pass


    def vstop(self):
        try:
            self.vrecording=False
            filename=filename=QFileDialog.getSaveFileName(self, 'Save File','', 'WAV (*.wav)')[0]
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
            wf = wave.open(filename, 'wb')
            wf.setnchannels(2)
            wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.vframes))
            wf.close()
            self.infowin.append('Recording Stoped')
        except Exception as e:print(e)


    def snap(self):
        try:
            self.hide()
            QtCore.QTimer.singleShot(500, self.snap2)
        except Exception as e:print(e)

    def record(self):
        filename=filename=QFileDialog.getSaveFileName(self, 'Save File','', 'MP4 (*.mp4)')[0]
        SCREEN_SIZE = (GetSystemMetrics(0),GetSystemMetrics(1))
        self.recorder = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*"XVID"), 20.0, (SCREEN_SIZE))
        self.t1=threading.Thread(target=self.startrecord)
        self.t1.start()


    def startrecord(self):
        try:
            self.infowin.append('Recording Started')
            self.recording=True
            while self.recording==True:
                img = pyautogui.screenshot()
                self.recorder.write(cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB))

        except Exception as e:print(e)
    def stoprecord(self):
        self.infowin.append('Recording Stoped')
        try:
            self.recording=False
            QtCore.QTimer.singleShot(500, lambda:print(self.t1.is_alive()))
            cv2.destroyAllWindows()
            self.recorder.release()
        except Exception as e:print(e)
    def pauserecord(self):
        self.infowin.append('Recording Paused')
        self.recording=False


    def select_folder(self):
        try:
            self.imagepath = str(QFileDialog.getExistingDirectory(self, "Select Directory"))+'/'
            self.images=[i for i in os.listdir(self.imagepath) if i[-4:] in['.png','.PNG','.JPG']]
            self.current=''
            self.next()
        except Exception as e:print(e)

    def fit(self):
        try:
            w=self.sw.viewport().width()
            h=self.sw.viewport().height()
            self.l.setPixmap(self.pixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio))
            self.l.setFixedWidth(self.sw.viewport().width())
            self.l.setFixedHeight(self.sw.viewport().height())
            self.l.setFixedWidth(self.l.pixmap().width())
            self.l.setFixedHeight(self.l.pixmap().height())
        except Exception as e:print(e)

    def save(self):
        try:
            filename=QFileDialog.getSaveFileName(self, 'Save File')
            self.l.pixmap().save(filename[0])
            [self.imagepath,self.current]=os.path.split(filename[0])
            self.imagepath+='/'
            self.images=[i for i in os.listdir(self.imagepath) if i[-4:] in['.png','.PNG','.JPG']]
            self.save_comment()
            self.Show(self.imagepath,self.current)
        except Exception as e:print(e)

    def delete(self):
        if os.path.exists(self.imagepath+self.current):
            os.remove(self.imagepath+self.current)
        self.next()
        self.images=[i for i in os.listdir(self.imagepath) if i[-4:] in['.png','.PNG','.JPG']]

    def snap2(self):
        try:
            app=self.app
            self.pixmap = QScreen.grabWindow(app.primaryScreen(), app.desktop().winId())
            self.l.setPixmap(self.pixmap)
            self.l.setFixedWidth(self.pixmap.width())
            self.l.setFixedHeight(self.pixmap.height())
            self.l.setAlignment(Qt.AlignCenter)
            QtCore.QTimer.singleShot(500, lambda:self.show())
        except Exception as e:print(e)

    def draw(self):
        class win(QDialog):
            def __init__(self):
                super().__init__()
                self.painter = QtGui.QPainter(image)
                self.painter.setPen(QtGui.QPen(Qt.red, 3,Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

            def paintEvent(self, event):
                QtGui.QPainter(self).drawPixmap(self.rect(), image)

            def mousePressEvent(self, event):
                if (event.button() == Qt.LeftButton):self.lastPoint = event.pos()

            def mouseMoveEvent(self, event):
                try:
                    if (event.buttons() & Qt.LeftButton):
                        self.painter.drawLine(self.lastPoint, event.pos())
                        self.lastPoint = event.pos()
                        self.update()
                except Exception as e:print(e)
            def closeEvent(self, event):
                label1.setPixmap(image)
        label1=self.l
        image=self.pixmap
        win1=win()
        win1.resize(image.width(),image.height())
        win1.exec()

    def crop(self):
        try:
            self.currentQRect = self.currentQRubberBand.geometry()
            cropQPixmap = self.l.pixmap().copy(self.currentQRect)
            self.l.setPixmap(cropQPixmap)
            self.currentQRubberBand.hide()
            self.currentQRect=None
            self.pixmap =cropQPixmap
            self.l.setFixedWidth(self.l.pixmap().width())
            self.l.setFixedHeight(self.l.pixmap().height())
            #self.fit()
        except Exception as e:print(e)

    def next(self):
        try:
            if self.images==[]:return
            elif self.current=='': self.current=self.images[0]
            elif self.current==self.images[-1]:self.current=self.images[0]
            elif self.current in self.images:self.current= self.images[self.images.index(self.current)+1]
            else:return
            self.Show(self.imagepath,self.current)

        except Exception as e:print(e)

    def previous(self):
        try:

            if self.images==[]:return
            elif self.current=='': self.current=self.images[0]
            elif self.current==self.images[0]:self.current=self.images[-1]
            elif self.current in self.images:self.current= self.images[self.images.index(self.current)-1]
            else:return
            self.Show(self.imagepath,self.current)
        except Exception as e:print(e)

    def Show(self,folder,img):
        self.pixmap = QPixmap(folder+img)
        self.l.setPixmap(self.pixmap)
        self.TE.setPlainText(self.commentdata.get(img,['',''])[1])
        self.sbar.showMessage(folder+img)
        self.l.setFixedWidth(self.l.pixmap().width())
        self.l.setFixedHeight(self.l.pixmap().height())
        self.update()
    def Show2(self):
        self.l.setPixmap(self.pixmap)
        self.l.setFixedWidth(self.l.pixmap().width())
        self.l.setFixedHeight(self.l.pixmap().height())
        self.update()


    def getcomment(self):
        try:
            if not os.path.exists("imagecomments.csv"):self.commentdata={};return
            csvfile= open('imagecomments.csv', newline='')
            self.commentdata={r[0]:r for r in csv.reader(csvfile) if r!=[]}
            csvfile.close()

        except Exception as e:print(e)

    def save_comment(self):
        try:
            self.commentdata[self.current]=[self.current,self.TE.toPlainText()]
            f = open('imagecomments.csv', 'w')
            writer = csv.writer(f)
            writer.writerows(self.commentdata.values())
            f.close()
        except Exception as e:print(e)


    def mousePressEvent(self, event):
        try:
            if (event.button() == Qt.LeftButton):
                self.originQPoint = event.pos()
                self.currentQRubberBand.setGeometry(QtCore.QRect(self.originQPoint, QtCore.QSize()))
                self.currentQRubberBand.show()
        except Exception as e:print(e)
    def mouseMoveEvent(self, event):
        try:
            if (event.buttons() & Qt.LeftButton):
                self.currentQRubberBand.setGeometry(QtCore.QRect(self.originQPoint, event.pos()).normalized())
        except Exception as e:print(e)





class facerecognize():
    def __init__(self):
        self.dataset="D:\\datasets\\"
        self.module=self.dataset+"encoding1.pickle"

    def register(self):
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)
        path = self.dataset# path were u want store the data set
        id = input('enter user name')

        try:
            os.mkdir(path+str(id))
            print("Directory " , path+str(id),  " Created ")
        except FileExistsError:
            print("Directory " , path+str(id) ,  " already exists")
        sampleN=0;

        while 1:
            ret, img = cap.read()
            frame = img.copy()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                sampleN=sampleN+1;
                cv2.imwrite(path+str(id)+ "\\" +str(sampleN)+ ".jpg", gray[y:y+h, x:x+w])
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                cv2.waitKey(100)
            cv2.imshow('img',img)
            cv2.waitKey(1)
            if sampleN > 40:break

        cap.release()
        cv2.destroyAllWindows(),

    def read(self):
        imagepaths = list(paths.list_images(dataset))
        knownEncodings = []
        knownNames = []
        for (i, imagePath) in enumerate(imagepaths):
            print("[INFO] processing image {}/{}".format(i + 1,len(imagepaths)))
            name = imagePath.split(os.path.sep)[-2]
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb, model= "hog")
            encodings = face_recognition.face_encodings(rgb, boxes)
            for encoding in encodings:
               knownEncodings.append(encoding)
               knownNames.append(name)
               print("[INFO] serializing encodings...")
               data = {"encodings": knownEncodings, "names": knownNames}
               output = open(self.module, "wb")
               pickle.dump(data, output)
               output.close()

    def recognize(self):

        encoding = self.module
        data = pickle.loads(open(encoding, "rb").read())
        cap = cv2.VideoCapture(0)
        if cap.isOpened :ret, frame = cap.read()
        else:ret = False
        while(ret):
          ret, frame = cap.read()
          frame = cv2.flip(frame, 90)
          rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
          rgb = imutils.resize(frame, width=400)
          r = frame.shape[1] / float(rgb.shape[1])
          boxes = face_recognition.face_locations(rgb, model= "hog")
          encodings = face_recognition.face_encodings(rgb, boxes)
          names = []
          for encoding in encodings:
                    matches = face_recognition.compare_faces(np.array(encoding),np.array(data["encodings"]))
                    name = "Unknown"
                    if True in matches:
                        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                        counts = {}
                        for i in matchedIdxs:
                            name = data["names"][i]
                            counts[name] = counts.get(name, 0) + 1
                            name = max(counts, key=counts.get)
                    names.append(name)
          for ((top, right, bottom, left), name) in zip(boxes, names):
              top = int(top * r)
              right = int(right * r)
              bottom = int(bottom * r)
              left = int(left * r)
              cv2.rectangle(frame, (left, top), (right, bottom),(0, 255, 0), 2)
              y = top - 15 if top - 15 > 15 else top + 15
              cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)

          cv2.imshow("Frame", frame)
          if cv2.waitKey(1) == 27:break#esc
        cv2.destroyAllWindows()
        cap.release()




def stored(x):
    try:base_path = sys._MEIPASS
    except Exception:base_path = os.path.abspath(".")
    return os.path.join(base_path,'stored/'+x).replace('\\','/')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window=image_editor()
    window.showMaximized()
    sys.exit(app.exec_())
