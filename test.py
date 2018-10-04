from image_restorer import*
import os
import cv2

def main():

    cur_dir = os.getcwd()
    image_name = cur_dir + '/images/circle_noise_gauss.png'
    rest_method = 'Difussion'
    steps = 10
    image = cv2.imread(image_name)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    plt.figure()
    for i in range(steps):
        image = restore(image, rest_method)
        plt.plot(image[int(len(image)/2)], 'b')
        plt.pause(0.0001)
        plt.cla()
    plt.show()
if __name__ == '__main__':
    main()

