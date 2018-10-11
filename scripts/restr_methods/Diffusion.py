# -*- coding: utf-8 -*-
"""
@author: jl
"""
import numpy as np
import copy
import cv2
from matplotlib import pyplot as plt


# --- diffusion with cyclical boundary conditions---
def Diffusion_c(im, D, dx):

    """
    The application of diffusion using nested loops and cyclical boundary conditions
    :param im: Image in array form
    :param D: Diffusion parameter
    :return: the array after a step of diffusion
    """


    im_var = im.copy()
    for i in range(len(im)):
        for j in range(len(im.T)):

            if i == 0:
                u1 = im[len(im) - 1, j]
            else:
                u1 = im[i - 1, j]

            if i == len(im) - 1:
                u2 = im[0, j]
            else:
                u2 = im[i + 1, j]

            if j == 0:
                u3 = im[i, len(im.T) - 1]
            else:
                u3 = im[i, j - 1]

            if j == len(im.T) - 1:
                u4 = im[i, 0]
            else:
                u4 = im[i, j + 1]

            u1 = int(u1)
            u2 = int(u2)
            u3 = int(u3)
            u4 = int(u4)

            u = (D/(dx**2))*(u1 + u2 + u3 + u4 - 4 * int(im[i, j]))
            im_var[i, j] = u

    im = im + im_var
    return im


# ----diffusion using static boundary condition----
def Difussion(im, D, dx):
    """
        The application of diffusion using nested loops and fixed boundary conditions
        :param im: Image in array form
        :param D: Diffusion parameter
        :return: the array after a step of diffusion
        """
    im_var = im.copy()
    for i in range(1, len(im) - 1):
        for j in range(1, len(im.T) - 1):

            u1 = im[i - 1, j]
            u2 = im[i + 1, j]
            u3 = im[i, j - 1]
            u4 = im[i, j + 1]

            u1 = int(u1)
            u2 = int(u2)
            u3 = int(u3)
            u4 = int(u4)

            u = (D / (dx ** 2)) * (u1 + u2 + u3 + u4 - 4 * int(im[i, j]))
            im_var[i, j] = u

    im = im + im_var
    return im


# ---diffusion using matrix method---
def Difussion_f(im, D, dx):
    """
        The application of diffusion using Matrix operations and fixed boundary conditions
        :param im: Image in array form
        :param D: Diffusion parameter
        :return: the array after a step of diffusion
        """
    im_var1 = im.copy()
    im_var2 = im.copy()

    a1 = np.multiply((D/dx**2), generate_matrix(len(im.T)))
    a2 = np.multiply((D/dx**2), generate_matrix(len(im)))

    for j in range(len(im)):
        u1 = a1.dot(im[j, :])
        im_var1[j, :] = u1
    for i in range(len(im[0])):
        u2 = a2.dot(im[:, i])
        im_var2[:, i] = u2

    im = im + im_var1 + im_var2

    return im

# function to generate a matrix for the diffusion in 1D
def generate_matrix(n):
    a = np.multiply(-2/1, np.identity(n))
    ide = np.multiply(1/1, np.identity(n-1)).tolist()

    for i in ide:
        i.append(0)

    ide.insert(0, np.zeros(n).tolist())
    ide = np.asarray(ide)
    m = a + ide + ide.T

    return m

def get_neighborhood(nd_idx, radius, image):
    u1 = image[nd_idx[0] + 1, nd_idx[1]]
    u2 = image[nd_idx[0] - 1, nd_idx[1]]
    u3 = image[nd_idx[0], nd_idx[1] + 1]
    u4 = image[nd_idx[0], nd_idx[1] - 1]

    return u1, u2, u3, u4



def impaint_Diff(image, mask):

    """
    Impainting using difussion
    :param image: image to imapaint
    :param mask: mask of which points are needed to be restored.
    :return: the image after a step of impainting using diffusion
    """
    im_new = np.zeros(np.shape(image))
    mask = mask.astype(np.bool)
    D = 1
    dx = 1
    p = 0.001
    mask_pts = np.array(np.where(mask)).T
    for mask_pt_n, mask_pt_idx in enumerate(mask_pts):

        u1, u2, u3, u4 = get_neighborhood(mask_pt_idx, 1, image)
        u = (D/dx**2)*np.average([u1, u2, u3, u4]) - 4 * p * int(image[mask_pt_idx[0], mask_pt_idx[1]])
        image[mask_pt_idx[0], mask_pt_idx[1]] = int(u)

    #image = image+im_new

    return image
