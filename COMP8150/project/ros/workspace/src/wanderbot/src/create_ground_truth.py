import numpy as np
import numpy.ma as ma

from image_util import *


# Determine RGB values and ranges for each class

def is_cylinder(rgb):
    CYLINDER_RGB = [[113, 113, 0]]

    return True


def is_sphere(rgb):
    return True


def is_cube(rgb):
    return True


def is_background(rgb):
    BACKGROUND_RGBS = [
        [178, 178, 178],  # Sky
        [102, 78, 31],  # Wall 1
        [116, 92, 45],  # Wall 2
        [55, 55, 55],  # Ground
    ]

    return True


def similarity(rgb, cmp_rgbs):
    min = 9999
    for cmp in cmp_rgbs:
        min = np.min([min, np.linalg.norm(rgb - cmp)])
    return min


image_specs = get_image_specs(images_dir, labels=get_categories(labels_file), scaling_factor=1)
target_spec = find_image_specs_by_id(image_specs, ['43'])
image = target_spec[0].data
image_orig = np.reshape(image, (480, 640, 3))
# norm_array = np.linalg.norm(image_orig - [178, 178, 178], axis=2)

# mask = np.ma.make_mask(norm_array < 10, copy=True, shrink=False, dtype=np.bool)
# mask = norm_array < 10
# mask = mask.astype(int)
# mask = np.repeat(mask[...,None],3,axis=2)

# n = np.linalg.norm(image_orig - [55,55,55], axis=2)
n = np.linalg.norm(image_orig - [178,178,178], axis=2)
mask = n < 20
NEW_PIXEL_VALUE = [255,255,255]
image_new = image_orig.copy()
image_new[mask] = NEW_PIXEL_VALUE

# cv2.imshow('original image', image_orig)
cv2.imshow('masked image', image_new)
cv2.waitKey(0)
