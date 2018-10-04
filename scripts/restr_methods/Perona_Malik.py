import numpy as np
from scipy import ndimage
def Perona_Malik(im, dd, delta, kappa):
    windows = [
        np.array([[0, 1, 0],
                  [0, -1, 0],
                  [0, 0, 0]]),
        np.array([[0, 0, 0],
                  [0, -1, 0],
                  [0, 1, 0]]),
        np.array([[0, 0, 0],
                  [0, -1, 1],
                  [0, 0, 0]]),
        np.array([[0, 0, 0],
                  [1, -1, 0],
                  [0, 0, 0]]),
        np.array([[0, 0, 1],
                  [0, -1, 0],
                  [0, 0, 0]]),
        np.array([[0, 0, 0],
                  [0, -1, 0],
                  [0, 0, 1]]),
        np.array([[0, 0, 0],
                  [0, -1, 0],
                  [1, 0, 0]]),
        np.array([[1, 0, 0],
                  [0, -1, 0],
                  [0, 0, 0]])]

    # approximate gradients
    nab = [ndimage.filters.convolve(im, w) for w in windows]

    # approximate diffusion function
    diff = [1 / (1 + (n / kappa) ** 2) for n in nab]

    # update image
    terms = [diff[i] * nab[i] for i in range(4)]
    terms += [(1 / (dd ** 2)) * diff[i] * nab[i] for i in range(4, 8)]
    im = im + delta * (sum(terms))

    return im




