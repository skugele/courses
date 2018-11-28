import numpy as np
import numpy.ma as ma

import matplotlib.pyplot as plt
from image_util import *

CYLINDER_CATEGORY_ID = 1
CUBE_CATEGORY_ID = 2
SPHERE_CATEGORY_ID = 3

N_CATEGORIES = 4 # Background has implicit category id = 0

DataSet = collections.namedtuple('DataSet', ['data_dirs', 'bgrs_dict'])

dataset1 = DataSet(data_dirs=['/var/local/data/skugele/COMP8150/project/room1/images'],
                   bgrs_dict={
                       CYLINDER_CATEGORY_ID: [[0, 113, 113]],
                       CUBE_CATEGORY_ID: [
                           [0, 0, 107],  # Red Cube
                           [107, 0, 0]  # Blue Cube
                       ],
                       SPHERE_CATEGORY_ID: [[0, 111, 0]]
                   }
                   )
dataset2 = DataSet(data_dirs=['/var/local/data/skugele/COMP8150/project/room2/images'],
                   bgrs_dict={
                       CYLINDER_CATEGORY_ID: [[0, 111, 0]],
                       CUBE_CATEGORY_ID: [[0, 0, 107]],
                       SPHERE_CATEGORY_ID: [
                           [107, 0, 0],  # Blue Sphere
                           [0, 113, 113]  # Yellow Sphere
                       ]
                   }
                   )

dataset3 = DataSet(data_dirs=['/var/local/data/skugele/COMP8150/project/cube_world/images'],
                   bgrs_dict={
                       CUBE_CATEGORY_ID: [
                           [107, 0, 0],  # Blue Cube
                           [0, 113, 113],  # Yellow Cube
                           [0, 0, 107],  # Red Cube
                           [0, 111, 0]  # Green Cube
                       ]
                   }
                   )

dataset4 = DataSet(data_dirs=['/var/local/data/skugele/COMP8150/project/cylinder_world/images'],
                   bgrs_dict={
                       CYLINDER_CATEGORY_ID: [
                           [107, 0, 0],  # Blue Cylinder
                           [0, 113, 113],  # Yellow Cylinder
                           [0, 0, 107],  # Red Cylinder
                           [0, 111, 0]  # Green Cylinder
                       ]
                   }
                   )

dataset5 = DataSet(data_dirs=['/var/local/data/skugele/COMP8150/project/sphere_world/images'],
                   bgrs_dict={
                       SPHERE_CATEGORY_ID: [
                           [107, 0, 0],  # Blue Sphere
                           [0, 113, 113],  # Yellow Sphere
                           [0, 0, 107],  # Red Sphere
                           [0, 111, 0]  # Green Sphere
                       ]
                   }
                   )

OUTPUT_DIR = '/var/local/data/skugele/COMP8150/project/combined'

TRAIN_OUT_DIR = os.path.join(OUTPUT_DIR, 'train')
TRAIN_GT_OUT_DIR = os.path.join(OUTPUT_DIR, 'trainannot')
TEST_OUT_DIR = os.path.join(OUTPUT_DIR, 'test')
TEST_GT_OUT_DIR = os.path.join(OUTPUT_DIR, 'testannot')
VAL_OUT_DIR = os.path.join(OUTPUT_DIR, 'validate')
VAL_GT_OUT_DIR = os.path.join(OUTPUT_DIR, 'validateannot')

OUT_DIRS = [TRAIN_OUT_DIR, TRAIN_GT_OUT_DIR,
            TEST_OUT_DIR, TEST_GT_OUT_DIR,
            VAL_OUT_DIR, VAL_GT_OUT_DIR]

TRAIN_MANIFEST_FILE = os.path.join(OUTPUT_DIR, 'train.txt')
TEST_MANIFEST_FILE = os.path.join(OUTPUT_DIR, 'test.txt')
VAL_MANIFEST_FILE = os.path.join(OUTPUT_DIR, 'validate.txt')

DISPLAY_RESULTS = False
WRITE_RESULTS = True

TRAIN_PERCENTAGE = 0.9
TEST_PERCENTAGE = 1 - TRAIN_PERCENTAGE
VALIDATE_PERCENTAGE = 0.1  # A percentage of the test data


def display_ground_truth(image):
    plt.imshow(ground_truth.squeeze(), cmap='gray', interpolation='bicubic')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.show()


def display_image(image, waittime):
    cv2.imshow('original image', image)
    cv2.waitKey(waittime)


scaling_factor = .25
dims = 480, 640
scaled_dims = map(lambda dim: int(dim * scaling_factor), dims)
n_rgb_channels = 3
n_grayscale_channels = 1
similarity_threshold = 45

if WRITE_RESULTS:
    for path in OUT_DIRS:
        os.mkdir(path)

count = 1

datasets = [
    dataset1,
    dataset2,
    dataset3,
    dataset4,
    dataset5
]

for dataset in datasets:
    for f in get_all_image_files(dataset.data_dirs):
        image = process_image(f, scaling_factor)
        image = np.reshape(image, newshape=(scaled_dims[0], scaled_dims[1], n_rgb_channels))

        # Create a grayscale image.  0 value is considered "background mask".  Other mask values
        # are set in the categories dict.
        ground_truth = np.zeros(shape=(scaled_dims[0], scaled_dims[1], n_grayscale_channels))

        # if image pixels are "similar enough" to that object class then set the ground truth
        # pixel values to the id for that class
        obj_classes = [0 for n in range(N_CATEGORIES)]
        for category_id, bgrs in dataset.bgrs_dict.iteritems():
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