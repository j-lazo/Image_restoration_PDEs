# -*- coding: utf-8 -*-
"""

@author: jl
"""

from scripts.restr_methods.Diffusion import*
from scripts.restr_methods.Perona_Malik import*
from scripts.restr_methods.image_imp import biharmonic_impainting
import matplotlib.pylab as plt


def image_restorer(image_n, method, impaint, image_mask, region=[], plots=True):
    
    """
    General function where the image and methods and managed
    :param image_n: the image in array form
    :param method: method to apply to the image
    :param impaint: if the operation to perform is impainting
    :param image_mask: mask if needed in the operation
    :param region: if only a region is selected in the form [x_min, y_min, x_max, y_max]
    :param plots: if plots needed will pop-up in a different window
    :return: the image restored according to the method selected and the value of xi for image painting
    """

    # if the operation to perform is painting in the missing regions
    if impaint is True:

        mask = image_mask
        im = impaint_f(image_n, mask, method)

        # -----Calculate Xi----
        en = np.count_nonzero(mask)
        if en == 1 or en == 0:
            en = 1.001

        sigma_sqr = (1/(en -1) * np.sum(mask - (np.sum(mask))/en) ** 2)
        xi = ((1/en)*(np.sum(image_n - mask)**2)) / sigma_sqr

    else:

        im = copy.copy(image_n)

        if region!= []:

            if len(im.shape) < 3:
                im = restore(image_n, method)

            else:
                # 2DO: implement the method also for RGB images
                # separation in RGB,
                Y = np.arange(im.shape[0])
                X = np.arange(im.shape[1])
                X, Y = np.meshgrid(X, Y)
                Z1 = im[..., 0]
                Z2 = im[..., 1]
                Z3 = im[..., 2]

                Z1 = restore(Z1, method)
                Z2 = restore(Z1, method)
                Z3 = restore(Z1, method)

        else:

            if len(im.shape) < 3:
                im = restore(im, method)

            else:
                Y = np.arange(im.shape[0])
                X = np.arange(im.shape[1])
                X, Y = np.meshgrid(X, Y)
                Z1 = im[..., 0]
                Z2 = im[..., 1]
                Z3 = im[..., 2]
                Z1 = restore(Z1, method)
                Z2 = restore(Z1, method)
                Z3 = restore(Z1, method)

        xi = 1.0

        if plots is True:
            Y = np.arange(im.shape[0])
            X = np.arange(im.shape[1])
            X, Y = np.meshgrid(X, Y)
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            surf = ax.plot_surface(X, Y, im, cmap='Blues', linewidth=0, antialiased=False)
            plt.show()
            print('Discrepancy Score:')
            print(xi)

    return im, xi


def impaint_f(image, mask, method):

    """
    If impainting is selected, applys the method selected
    :param image: image in array form
    :param mask: mask
    :param method: the method to apply for impainting
    :return: the array after the operation
    """

    if method == 'impaint_Diff':
        ima = impaint_Diff(image, mask)

    elif method == 'biharmonic_impainting':
        ima = biharmonic_impainting(image, mask)

    elif method == 'impaint_Perona_Malik':
        ima = impaint_Perona_Malik(image, mask)

    return ima


def restore(image, method):

    """
    the function restore should be used if what your image have is noise
    :param image: image in array form
    :param method: the method to apply for impainting
    :return: the array after the operation
    """
    ima = image

    if method == 'Diffusion':
        D = 1
        dx = 3
        ima = Difussion(image, D, dx)
        
    elif method == 'Diffusion_f':
        D = 1
        dx = 2.23
        ima = Difussion_f(image, D, dx)

    elif method == 'Diffusion_c':
        D = 1
        dx = 3
        ima = Difussion_f(image, D, dx)

    elif method == 'Perona_Malik':

        dd = np.sqrt(2)
        delta = 0.14
        kappa = 15
        ima = Perona_Malik(image, dd, delta, kappa)

    elif method == 'Perona_Malik_2':

        dd = np.sqrt(2)
        delta = 0.14
        kappa = 15
        ima = Perona_Malik_2(image, dd, delta, kappa)

    return ima

