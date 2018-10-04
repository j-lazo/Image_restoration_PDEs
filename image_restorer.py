# -*- coding: utf-8 -*-
"""

@author: jl
"""
import numpy as np
import cv2 
from scripts.restr_methods.Diffusion import*
from scripts.restr_methods.Perona_Malik import*
import os

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pylab as plt
from matplotlib import cm


def image_restorer(image_name, method, im_compare, plots=True, region=[]):

    im = copy.copy(image_name)
    im_comp = im_compare

    if not region is True:
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
        
    else:

        if (len(im.shape)<3):
            im_r = im[region[0]:region[1],region[2]:region[3]]
            im_r = restore(im_r, method)

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

    # calculate xi
    if np.array_equal(image_name, im_compare) is True:
        xi = 1.0
    else:
        en = np.count_nonzero(im_compare - image_name)
        sigma_sqr = (1/(en -1) * np.sum(im_comp - (np.sum(im_comp))/en) ** 2)
        xi = ((1/en)*(np.sum(im - im_comp)**2)) / sigma_sqr



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

