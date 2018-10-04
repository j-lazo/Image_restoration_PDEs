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

    nab = [ndimage.filters.convolve(im, w) for w in windows]
    gpm1 = [1 / (1 + (n / kappa) ** 2) for n in nab]
    res = [gpm1[i] * nab[i] for i in range(8)]
    im = im + delta * (sum(res))

    return im

def Perona_Malik_2(im, dd, delta, kappa):
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

    nab = [ndimage.filters.convolve(im, w) for w in windows]
    gpm2 = [np.exp(-(n/kappa)**2) for n in nab]
    res = [gpm2[i] * nab[i] for i in range(8)]
    im = im + delta*(sum(res))

    return im



