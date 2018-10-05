# -*- coding: utf-8 -*-
"""
@author: jl
"""
import numpy as np
import copy


# --- diffusion with cyclical boundary conditions---
def Diffusion_c(im, D, dx):
    
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


def generate_matrix(n):
    a = np.multiply(-2/1, np.identity(n))
    ide = np.multiply(1/1, np.identity(n-1)).tolist()

    for i in ide:
        i.append(0)
    
    ide.insert(0, np.zeros(n).tolist())
    ide = np.asarray(ide)
    m = a + ide + ide.T

    return m
