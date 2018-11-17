import numpy as np
import numpy.ma as ma

import matplotlib.pyplot as plt
from image_util import *

# Most probable RGB values for each object class
CYLINDER_BGRS = [[0, 113, 113]]  # Yellow Cylinder

CUBE_BGRS = [
    [0, 0, 107],  # Red Cube
    [107, 0, 0]  # Blue Cube
]

SPHERE_BGRS = [[0, 111, 0]]  # Green Sphere

BACKGROUND_BGRS = [
    [178, 178, 178],  # Sky
    [31, 78, 102],  # Wall 1
    [45, 92, 116],  # Wall 2
    [55, 55, 55],  # Ground
]

PARENT_DIR = '/var/local/data/skugele/COMP8150/project/images'

TRAIN_OUT_DIR = os.path.join(PARENT_DIR, 'train')
TRAIN_GT_OUT_DIR = os.path.join(PARENT_DIR, 'trainannot')
TEST_OUT_DIR = os.path.join(PARENT_DIR, 'test')
TEST_GT_OUT_DIR = os.path.join(PARENT_DIR, 'testannot')
VAL_OUT_DIR = os.path.join(PARENT_DIR, 'validate')
VAL_GT_OUT_DIR = os.path.join(PARENT_DIR, 'validateannot')

OUT_DIRS = [TRAIN_OUT_DIR, TRAIN_GT_OUT_DIR,
            TEST_OUT_DIR, TEST_GT_OUT_DIR,
            VAL_OUT_DIR, VAL_GT_OUT_DIR]

TRAIN_MANIFEST_FILE = os.path.join(PARENT_DIR, 'train.txt')
TEST_MANIFEST_FILE = os.path.join(PARENT_DIR, 'test.txt')
VAL_MANIFEST_FILE = os.path.join(PARENT_DIR, 'validate.txt')

DISPLAY_RESULTS = False
WRITE_RESULTS = True

TRAIN_PERCENTAGE = 0.8
TEST_PERCENTAGE = 1 - TRAIN_PERCENTAGE
VALIDATE_PERCENTAGE = 0.2  # A percentage of the test data


def display_ground_truth(image):
    plt.imshow(ground_truth.squeeze(), cmap='gray', interpolation='bicubic')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.show()


def display_image(image, waittime):
    cv2.imshow('original image', image)
    cv2.waitKey(waittime)


categories = {1: CYLINDER_BGRS, 2: CUBE_BGRS, 3: SPHERE_BGRS}  # Background BGRS implicitly have key = 0
n_categories = len(categories) + 1

scaling_factor = .25
dims = 480, 640
scaled_dims = map(lambda dim: int(dim * scaling_factor), dims)
n_rgb_channels = 3
n_grayscale_channels = 1
similarity_threshold = 40

if WRITE_RESULTS:
    for path in OUT_DIRS:
        os.mkdir(path)

count = 1
image_specs = get_image_specs(images_dir, labels=get_categories(labels_file), scaling_factor=scaling_factor)
for spec in image_specs:
    image = np.reshape(spec.data, newshape=(scaled_dims[0], scaled_dims[1], n_rgb_channels))

    # Create a grayscale image.  0 value is considered "background mask".  Other mask values
    # are set in the categories dict.
    ground_truth = np.zeros(shape=(scaled_dims[0], scaled_dims[1], n_grayscale_channels))

    # if image pixels are "similar enough" to that object class then set the ground truth
    # pixel values to the id for that class
    obj_classes = [0 for n in range(n_categories + 1)]
    for category_id, bgrs in categories.iteritems():
        for bgr in bgrs:
            norms = np.linalg.norm(image - bgr, axis=2)
            category_mask = norms < similarity_threshold
            ground_truth[category_mask] = category_id

            if True in category_mask:
                obj_classes[category_id] = 1
            else:
                obj_classes[0] = 1

    if DISPLAY_RESULTS:
        display_ground_truth(ground_truth)
        display_image(image, 0)

    # Randomly choose to assign to train, test
    is_train = np.random.uniform() < TRAIN_PERCENTAGE

    # Randomly split test data into test/validate
    is_validate = is_train and (np.random.uniform() < VALIDATE_PERCENTAGE)

    if WRITE_RESULTS:
        image_filename = os.path.join('image_{:07d}.png'.format(count))
        ground_truth_filename = 'image_gt_{:07d}.png'.format(count)

        # Update manifest
        manifest = VAL_MANIFEST_FILE if is_validate \
            else TRAIN_MANIFEST_FILE if is_train \
            else TEST_MANIFEST_FILE

        image_dir = VAL_OUT_DIR if is_validate \
            else TRAIN_OUT_DIR if is_train \
            else TEST_OUT_DIR

        ground_truth_dir = VAL_GT_OUT_DIR if is_validate \
            else TRAIN_GT_OUT_DIR if is_train \
            else TEST_GT_OUT_DIR

        image_filepath = os.path.join(image_dir, image_filename)
        ground_truth_filename = os.path.join(ground_truth_dir, ground_truth_filename)

        with open(manifest, 'a') as fd:
            fd.write(' '.join([image_filepath, ground_truth_filename, ''.join(map(str, obj_classes)), '\n']))

        # Save image and ground truth
        cv2.imwrite(image_filepath, image)
        cv2.imwrite(ground_truth_filename, ground_truth)

    count += 1
