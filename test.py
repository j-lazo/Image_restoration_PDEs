from image_restorer import*
import os
import cv2

def main():

    cur_dir = os.getcwd()
    #
    # -----parameterst that you can change-----
    image_name = cur_dir + '/images/circle_noise_gauss.png'
    rest_method = 'Difussion'
    steps = 10
    #
    #

    image = cv2.imread(image_name)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    for i in range(steps):
        image = restore(image, rest_method)

if __name__ == '__main__':
    main()

