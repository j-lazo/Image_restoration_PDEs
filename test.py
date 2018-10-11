from image_restorer import*
from scripts.restr_methods.Diffusion import*
import os
import cv2
from matplotlib import pyplot as plt


def main():

    cur_dir = os.getcwd()
    #
    # -----parameterst that you can change-----
    image_name = cur_dir + '/scripts/restr_methods/grafitti2.png'
    original_image = cur_dir + '/scripts/restr_methods/mini_land2.png'
    rest_method = 'Difussion'
    steps = 1
    plot = False

    image = cv2.imread(image_name)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    original = cv2.imread(original_image)
    original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

    for i in range(steps):
        imap = impaint_Diff(image, original)

    if plot is True:
        plt.figure()
        plt.imshow(imap, cmap='gray')
        plt.show()


if __name__ == '__main__':
    main()

