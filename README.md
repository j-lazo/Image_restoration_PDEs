# Image_restoration_PDEs
## Image restoration using partial differential equations

This is a simple project to test different image restoration methods, based on PDEs. The Image restoring method used here are simple diffusion and the Perona-Malik method. To run the programm **main.py**, this will launch a GUI in which you can choose the different options, if you prefer you can also run the script **test.py** and in this one change the parameters of `image_name`, `rest_method` and `steps`. 

### Libraries needed

This program was developed using **Python3** and uses the libraries 
..* Numpy
..* OpenCv2
..* Scipy
..* PyQt5

### How to use the GUI

If you run the program **main.py** it will launch a GUI developed in PyQt5. The steps to follow are the next:
1. Pres *Ctrl + L* or click the button `[...]` to load a damaged image or open the menu file and select `Load Image`. The program only supporst *.png*, *.bmp* and *.jpg* formats for the moment. 
2. Once you have choosen in the box `Select a Method` select a method to restore the image. 
3. Select the number of steps on which the restoration method will be iterated. 
4. If you have the original image before damaged and you want to select the Discrepancy Score, check the box `Compare with original?`
5. Click `Go` and wait for results. 

 




