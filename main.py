import sys
import design
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QAction, QMessageBox
from PyQt5.uic.properties import QtGui

class ExampleApp(QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super(ExampleApp, self).__init__()
        self.setupUi(self)
        
	
        # Actions
        self.actionQuit.setShortcut('Ctrl+Q')
        self.actionQuit.setStatusTip('Leave the app')
        self.actionQuit.triggered.connect(self.close_application)
        self.actionNew.setShortcut('Ctrl+N')
        self.actionNew.setStatusTip('New simulation')
        self.actionNew.triggered.connect(self.new_simulation)
        self.actionLoad_New_Image.setShortcut('Ctrl+L')
        self.actionLoad_New_Image.setStatusTip('Load New Image')
        self.actionLoad_New_Image.triggered.connect(self.load_image)
        self.actionSave_Image.setShortcut('Ctrl+S')
        self.actionSave_Image.setStatusTip('Save image')
        self.actionSave_Image.triggered.connect(self.save_image)

        self.actionRestore_Image.setShortcut('Shift+Ctrl+R')
        self.actionRestore_Image.setStatusTip('Save image')
        self.actionRestore_Image.triggered.connect(self.restore_image)
        self.actionSelect_specific_area.setShortcut('Shift+Ctrl+A')
        self.actionSelect_specific_area.setStatusTip('Save image')
        self.actionSelect_specific_area.triggered.connect(self.select_region)

        
        self.actionQuit.triggered.connect(self.close_application)

        scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(scene)
        #pen = QtGui.QPen(QtCore.Qt.green)

        #side = 20

        #for i in range(16):
        #    for j in range(16):
        #        r = QtCore.QRectF(QtCore.QPointF(i*side, j*side), QtCore.QSizeF(side, side))
        #        scene.addRect(r, pen)



    def close_application(self):

        choice = QMessageBox.question(self, 'Close!',
                                     "Are you sure you want  to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if choice == QMessageBox.Yes:
            sys.exit()
        else:
            pass
    def new_simulation(self):
        pass
    
    def save_image(self):
        pass
        
    def load_image(self):
        
        self.setScene(QGraphicsScene())
        self.path = QPainterPath()
        self.item = GraphicsPathItem()
        self.scene().addItem(self.item)
        pass
    
    def restore_image(self):
        pass
    
    def select_region():
        pass
        


def main():
    app = QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
