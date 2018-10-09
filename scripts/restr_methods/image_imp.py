import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve
import scipy.ndimage as ndi
from scipy.ndimage.filters import laplace, correlate1d
from skimage.measure import label


def _get_neighborhood(nd_idx, radius, nd_shape):
    bounds_lo = (nd_idx - radius).clip(min=0)
    bounds_hi = (nd_idx + radius + 1).clip(max=nd_shape)
    return bounds_lo, bounds_hi


def lambd(matr):
    return



def biharmonic(img, mask, out, limits):

    matrix_unknown = sparse.lil_matrix((np.sum(mask), img.size))
    matrix_known = sparse.lil_matrix((np.sum(mask), img.size))

    mask_i = np.ravel_multi_index(np.where(mask), mask.shape)
    mask_pts = np.array(np.where(mask)).T

    # Iterate over masked points
    for mask_pt_n, mask_pt_idx in enumerate(mask_pts):

        # Get bounded neighborhood of selected radius
        low_lim, hi_lim = _get_neighborhood(mask_pt_idx, 2, img.shape)

        neigh_coef = np.zeros(hi_lim - low_lim)
        neigh_coef[tuple(mask_pt_idx - low_lim)] = 1
        neigh_coef = laplace(laplace(neigh_coef))
        it_inner = np.nditer(neigh_coef, flags=['multi_index'])
        for coef in it_inner:
            if coef == 0:
                continue
            tmp_pt_idx = np.add(low_lim, it_inner.multi_index)
            tmp_pt_i = np.ravel_multi_index(tmp_pt_idx, mask.shape)

            if mask[tuple(tmp_pt_idx)]:
                matrix_unknown[mask_pt_n, tmp_pt_i] = coef
            else:
                matrix_known[mask_pt_n, tmp_pt_i] = coef

    flat_diag_image = sparse.dia_matrix((img.flatten(), np.array([0])),
                                        shape=(img.size, img.size))

    # Calculate right hand side as a sum of known matrix's columns
    matrix_known = matrix_known.tocsr()
    rhs = -(matrix_known * flat_diag_image).sum(axis=1)

    # Solve linear system for masked points
    matrix_unknown = matrix_unknown[:, mask_i]
    matrix_unknown = sparse.csr_matrix(matrix_unknown)
    result = spsolve(matrix_unknown, rhs)

    result = result.ravel()

    for mask_pt_n, mask_pt_idx in enumerate(mask_pts):
        out[tuple(mask_pt_idx)] = result[mask_pt_n]

    return out


def biharmonic_impainting(img, mask):

    mask = mask.astype(np.bool)
    kernel = ndi.morphology.generate_binary_structure(mask.ndim, 1)
    mask_dilated = ndi.morphology.binary_dilation(mask, structure=kernel)
    mask_labeled, num_labels = label(mask_dilated, return_num=True)
    mask_labeled *= mask

    img = img[..., np.newaxis]
    out = np.copy(img)
    for idx_channel in range(img.shape[-1]):
        known_points = img[..., idx_channel][~mask]
        limits = (np.min(known_points), np.max(known_points))
        for idx_region in range(1, num_labels+1):
            mask_region = mask_labeled == idx_region
            biharmonic(
                img[..., idx_channel], mask_region,
                out[..., idx_channel], limits)
    out = out[..., 0]

    return out

