import sys
import os
import cv2
import scripts.design as design
from image_restorer import*
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMenu, QMainWindow, QPushButton, QAction, QMessageBox
from PyQt5.QtWidgets import QFileDialog, QApplication, QVBoxLayout, QSizePolicy, QWidget

class ExampleApp(QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super(ExampleApp, self).__init__()
        self.setupUi(self)
        self.file_name = 'images/white.png'
        self.save_name = ''
        self.image_restored = 0
        self.restoration_method = ''
        
        # ----Actions---
        
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
        self.actionSelect_specific_area.setStatusTip('Select are')
        self.actionSelect_specific_area.triggered.connect(self.select_region)

        #self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)

        # ---Buttons---
       
        self.toolButton.clicked.connect(self.load_image)
        self.spinBox.setValue(1)
        self.spinBox.setMinimum(1)
        self.comboBox.activated.connect(self.handleActivated)
        self.comboBox.addItems(['Select a Method',
                                'Diffusion',
                                'Diffusion_f',
                                'Diffusion_c',
                                'Perona_Malik',
                                'Perona_Malik_2'])
        self.pushButton.clicked.connect(self.restore_image)
        self.pushButton_2.clicked.connect(self.save_image)
        self.spinBox.setMaximum(1000)

        pixmap = QPixmap(self.file_name)
        self.label_6.setPixmap(pixmap) 
        self.label_7.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        self.show()

    def close_application(self):
        choice = QMessageBox.question(self, 'Close!',
                                     "Are you sure you want to quit?", QMessageBox.Yes |
                                     QMessageBox.No)
        if choice == QMessageBox.Yes:
            sys.exit()
        else: 
            pass
        
        self.show()
        
    def new_simulation(self):
        self.spinBox.setValue(1)
        self.label_5.setText('0.0')
        self.progressBar.setValue(0)
        self.progressBar.setProperty("value", 0)
        pixmap = QPixmap('white.png')
        self.label_6.setPixmap(pixmap) 
        self.label_7.setPixmap(pixmap) 
        self.resize(pixmap.width(),pixmap.height())
        self.show()      
    
    def handleActivated(self, index):
        pass

    def save_image(self):
        save_name, _ = QFileDialog.getSaveFileName(self, 'Save Image')
        if save_name:
            cv2.imwrite(save_name, self.image_restored)
        self.show()

    def load_image(self):
        self.progressBar.setValue(0)
        self.label_5.setText('0.0')
        ext_options = ['.png', '.jpg', '.bmp']
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        name, _ = QFileDialog.getOpenFileName(self, "Open", "",
                                                "All Files (*);;Python Files (*.py);;PNG (*.png);;JPG (*.jpg);;BMP (*.bmp)", 
                                                options=options)
        self.file_name = name
        if name:
            if name[-4:] not in ext_options:
                im_choice = QMessageBox.question(self, 'Error!',
                                         "The file selected is not an image or the format is not supported", 
                                         QMessageBox.Ok)    
            else:
                pixmap = QPixmap(str(name))
                self.label_6.setPixmap(pixmap)
                pixmap1 = QPixmap('images/white.png')
                self.label_7.setPixmap(pixmap1)
                self.resize(pixmap.width(), pixmap.height())
                self.show()
        else:
            pass
        #self.show()

    def restore_image(self):
        new_ima = QPixmap('temp/white.png')
        self.label_7.setPixmap(new_ima)
        self.progressBar.setValue(0)

        # --- if there is an image to compare with
        if self.checkBox.isChecked() is True:
            QMessageBox.question(self, 'Atention!',
                                 "Select the original image to compare with",
                                 QMessageBox.Ok)

            ext_options = ['.png', '.jpg', '.bmp']
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            im_comparison, _ = QFileDialog.getOpenFileName(self, "Open", "",
                                                           "All Files (*);;Python Files (*.py);;PNG (*.png);;JPG (*.jpg);;BMP (*.bmp)",
                                                           options=options)

            if im_comparison:
                if im_comparison[-4:] not in ext_options:
                    QMessageBox.question(self, 'Error!',
                                         "The file selected is not an image or the format is not supported",
                                         QMessageBox.Ok)

            else:
                im_comparison = self.file_name
            self.show()
        else:
            im_comparison = self.file_name
            self.checkBox.setChecked(False)

        if self.comboBox.currentText() != 'Select a Method':
            # ------- do the restoration------

            image = cv2.imread(self.file_name)
            ima = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            im_comp = cv2.imread(im_comparison)
            im_comp = cv2.cvtColor(im_comp, cv2.COLOR_BGR2GRAY)

            if np.shape(ima) != np.shape(im_comp):

                QMessageBox.question(self, 'Error!',
                                     "Error, the image to compare with is not the same size as the image to restore",
                                     QMessageBox.Ok)

            else:

                for i in range(self.spinBox.value()):
                    self.progressBar.setValue(int(100*i/self.spinBox.value()))
                    ima, xi = image_restorer(ima, self.comboBox.currentText(), im_comp, plots=False)

                self.progressBar.setValue(100)
                self.image_restored = ima
                self.label_5.setText(str(xi))
                cv2.imwrite("".join([os.getcwd(), '/temp/', 'temp.png']), ima)
                new_ima = QPixmap('temp/temp.png')
                self.label_7.setPixmap(new_ima)

        else:
            QMessageBox.question(self, 'Error!',
                                         "Select a restoration method", 
                                         QMessageBox.Ok)  
    
    def select_region(self):

        def mousePressEvent(self, event):

            if event.button() == Qt.LeftButton:
                self.origin = QPoint(event.pos())
                self.rubberBand.setGeometry(QRect(self.origin, QSize()))
                self.rubberBand.show()

        def mouseMoveEvent(self, event):

            if not self.origin.isNull():
                self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())

        def mouseReleaseEvent(self, event):

            if event.button() == Qt.LeftButton:
                self.rubberBand.hide()


def main():
    app = QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
