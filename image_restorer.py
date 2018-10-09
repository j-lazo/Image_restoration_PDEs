# -*- coding: utf-8 -*-
"""

@author: jl
"""

from scripts.restr_methods.Diffusion import*
from scripts.restr_methods.Perona_Malik import*
from scripts.restr_methods.image_imp import biharmonic_impainting
import matplotlib.pylab as plt


def image_restorer(image_name, method, impaint, im_compare, region=[], plots=True):

    if impaint is True:
        #mask = im_compare - image_name
        mask = im_compare
        im = impaint_f(image_name, mask, method)

        # Calculate Xi
        en = np.count_nonzero(mask)
        if en == 1 or en == 0:
            en = 1.001

        sigma_sqr = (1/(en -1) * np.sum(mask - (np.sum(mask))/en) ** 2)
        xi = ((1/en)*(np.sum(image_name - mask)**2)) / sigma_sqr

    else:

        im = copy.copy(image_name)
        im_comp = im_compare
        if region != []:
            if len(im.shape) < 3:
                # im_r = im[region[1]:region[3], region[0]:region[2]]
                im_r = restore(im_r, method)
                # im[region[1]:region[3], region[0]:region[2]] = im_r
                # cv2.rectangle(im, (region[0], region[1]), (region[2], region[3]), (0, 211, 211), 1)

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

        xi = 0.0

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

    if method == 'impaint_Diff':
        ima = impaint_Diff(image, mask)

    elif method == 'biharmonic_impainting':
        ima = biharmonic_impainting(image, mask)

    elif method == 'impaint_Perona_Malik':
        ima = impaint_Perona_Malik(image, mask)

    return ima


def restore(image, method):
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

