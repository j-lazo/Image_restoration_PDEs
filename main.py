import sys
import os
import cv2
import scripts.design as design
from image_restorer import*
from PyQt5.Qt import Qt, QPoint, QRubberBand, QRect, QSize
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen, QColor, QPolygon
from PyQt5.QtWidgets import QMenu, QMainWindow, QPushButton, QAction, QMessageBox
from PyQt5.QtWidgets import QFileDialog, QApplication, QVBoxLayout, QSizePolicy, QWidget, QRubberBand



class ExampleApp(QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        super(ExampleApp, self).__init__()
        self.setupUi(self)
        self.file_name = 'images/white.png'
        self.save_name = ''
        self.image_restored = 0
        self.restoration_method = ''
        self.ext_options = ['.png', '.jpg', '.bmp']
        self.origin = QPoint()
        self.region_select = False
        self.points = QPolygon()
        self.region_restore = []
        self.x1, self.x2, self.y1, self.y2 = 0, 0, 0, 0

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
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)

        # ---Buttons---
       
        self.toolButton.clicked.connect(self.load_image)
        self.spinBox.setValue(1)
        self.spinBox.setMinimum(1)
        self.comboBox.activated.connect(self.handleActivated)
        # the restore and imapinting functions avialables.
        self.comboBox.addItems(['Select a Method',
                                'Diffusion',
                                'Diffusion_f',
                                'Diffusion_c',
                                'Perona_Malik',
                                'Perona_Malik_2',
                                'impaint_Diff',
                                'biharmonic_impainting',
                                'impaint_Perona_Malik'])

        self.pushButton.clicked.connect(self.restore_image)
        self.pushButton_2.clicked.connect(self.save_image)
        self.spinBox.setMaximum(100000)
        pixmap = QPixmap(self.file_name)
        self.label_6.setPixmap(pixmap) 
        self.label_7.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        self.show()

    # -----Functions of the GUI -----

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
        self.origin = QPoint()
        self.spinBox.setValue(1)
        self.label_5.setText('0.0')
        self.progressBar.setValue(0)
        self.progressBar.setProperty("value", 0)
        pixmap = QPixmap(self.file_name)
        self.label_6.setPixmap(pixmap)
        self.label_7.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        self.region_restore = []
        self.show()      

    def handleActivated(self, index):
        pass

    def save_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        save_name, _ = QFileDialog.getSaveFileName(self, 'Save Image', "",
                                                   "All Files (*);;Python Files (*.py);;PNG (*.png);;JPG (*.jpg);;BMP (*.bmp)",
                                                   options=options)
        if save_name:
            cv2.imwrite(save_name, self.image_restored)
        self.show()

    def load_image(self):
        self.origin = QPoint()
        self.progressBar.setValue(0)
        self.label_5.setText('0.0')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        name, _ = QFileDialog.getOpenFileName(self, "Open", "",
                                                "All Files (*);;Python Files (*.py);;PNG (*.png);;JPG (*.jpg);;BMP (*.bmp)", 
                                                options=options)
        self.file_name = name
        if name:
            if name[-4:] not in self.ext_options:
                im_choice = QMessageBox.question(self, 'Error!',
                                         "The file selected is not an image or the format is not supported", 
                                         QMessageBox.Ok)    
            else:
                pixmap = QPixmap(str(name))
                self.label_6.setPixmap(pixmap)
                pixmap1 = QPixmap('images/white.png')
                self.label_7.setPixmap(pixmap1)
                self.region_restore = []
                self.resize(pixmap.width(), pixmap.height())
                self.show()
        else:
            pass
        #self.show()

    def restore_image(self):
        
        # the function that calls the restoration function
        new_ima = QPixmap('temp/white.png')
        self.label_7.setPixmap(new_ima)
        self.progressBar.setValue(0)

        # --- if there is an image to compare with
        if self.checkBox.isChecked() is True:

            im_comparison = self.load_compare()

            if im_comparison:
                if im_comparison[-4:] not in self.ext_options:
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
                                     "The image to compare with is not the same size as the image to restore",
                                     QMessageBox.Ok)

                im_comparison = self.load_compare()
                im_comp = cv2.imread(im_comparison)
                im_comp = cv2.cvtColor(im_comp, cv2.COLOR_BGR2GRAY)

            else:
                self.region_select = False
                if self.region_restore != []:
                        imo = copy.copy(ima)
                        x1 = min(self.region_restore[0], self.region_restore[2])
                        y1 = min(self.region_restore[1], self.region_restore[3])
                        x2 = max(self.region_restore[0], self.region_restore[2])
                        y2 = max(self.region_restore[1], self.region_restore[3])
                        ima = ima[y1:y2, x1:x2]

                mask = im_comp - ima
                if self.restoration_method == 'biharmonic_impainting':
                    maxi = 1
                else:
                    maxi = self.spinBox.value()

                for i in range(maxi):
                    self.restoration_method = self.comboBox.currentText()
                    self.progressBar.setValue(int(100*i/self.spinBox.value()))
                    ima, xi = image_restorer(ima,
                                             self.restoration_method,
                                             self.checkBox.isChecked(),
                                             mask, [], plots=False)
                    #mask = ima - imag

                if self.region_restore != []:
                    imo[y1:y2, x1:x2] = ima
                    ima = copy.copy(imo)

                self.progressBar.setValue(100)
                self.image_restored = ima
                self.label_5.setText(str(xi))

                cv2.imwrite("".join([os.getcwd(), '/temp/', 'temp.jpg']), ima)
                new_ima = QPixmap('temp/temp.jpg')
                self.label_7.setPixmap(new_ima)

        else:
            QMessageBox.question(self, 'Error!',
                                         "Select a restoration method", 
                                         QMessageBox.Ok)

    def load_compare(self):

        QMessageBox.question(self, 'Atention!',
                             "Select the original image to compare with",
                             QMessageBox.Ok)

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        im_comparison, _ = QFileDialog.getOpenFileName(self, "Open", "",
                                                       "All Files (*);;Python Files (*.py);;PNG (*.png);;JPG (*.jpg);;BMP (*.bmp)",
                                                       options=options)

        self.show()
        return im_comparison

    def select_region(self):
        self.region_select = True

    def mousePressEvent(self, event):

        if self.region_select is True:
            if event.button() == Qt.LeftButton:
                self.origin = QPoint(event.pos())
                if self.origin.x() >= self.label_6.x() and self.origin.y() >= self.label_6.y() + 20:
                    self.rubberBand.setGeometry(QRect(self.origin, QPoint(event.x(), event.y())))
                    self.rubberBand.show()
                else:
                    self.origin = QPoint()

    def mouseMoveEvent(self, event):

        if not self.origin.isNull():
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):

        max_x = QPixmap(self.file_name).width()
        max_y = QPixmap(self.file_name).height()
        min_x = self.label_6.x()
        min_y = self.label_6.y() + 20

        self.x1 = self.origin.x() - self.label_6.x()
        self.y1 = self.origin.y() - self.label_6.y() - 20
        self.x2 = event.x() - self.label_6.x()
        self.y2 = event.y() - self.label_6.y() - 20

        if event.x() > max_x:
            self.rubberBand.setGeometry(QRect(self.origin, QPoint(max_x + self.label_6.x(), event.y())))

        if event.y() > max_y:
            self.rubberBand.setGeometry(QRect(self.origin, QPoint(event.x(), 20 + max_y + self.label_6.y())))

        if event.y() > max_y and event.x() > max_x:
            self.rubberBand.setGeometry(QRect(self.origin, QPoint(max_x + self.label_6.x(), 20 + max_y + self.label_6.y())))

        if event.x() < min_x:
            self.rubberBand.setGeometry(QRect(self.origin, QPoint(min_x, event.y())))

        if event.y() < min_y:
            self.rubberBand.setGeometry(QRect(self.origin, QPoint(event.x(), min_y)))

        if event.y() < min_y and event.x() < min_x:
            self.rubberBand.setGeometry(QRect(self.origin, QPoint(min_x, min_y)))

        if event.button() == Qt.LeftButton and self.region_select is True and not self.origin.isNull():
            choice_rectangle = QMessageBox.question(self, 'Question',
                                          "Is this the region you want to restore?",
                                           QMessageBox.Yes | QMessageBox.No)

            if choice_rectangle == QMessageBox.Yes:

                self.region_select = False
                # ----------Draw the area-----------
                temp_im = cv2.imread(self.file_name)
                cv2.rectangle(temp_im, (self.x1, self.y1), (self.x2, self.y2), (148, 0, 211), 1)
                cv2.rectangle(temp_im, (self.x1+1, self.y1+1), (self.x2+1, self.y2+1), (0, 211, 211), 1)
                cv2.imwrite('temp/temp0.png', temp_im)
                temp_pixmap = QPixmap('temp/temp0.png')
                self.label_6.setPixmap(temp_pixmap)
                self.region_restore = [self.x1,
                                       self.y1,
                                       self.x2,
                                       self.y2]

            else:
                pass

        self.rubberBand.hide()
        self.origin = QPoint()



def main():
    app = QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
