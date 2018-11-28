from image_util import get_all_image_files, process_image
import numpy as np

dirs = [
    '/var/local/data/skugele/COMP8150/project/combined/trainannot'
]

BACKGROUND_CATEGORY_ID = 0
CYLINDER_CATEGORY_ID = 1
CUBE_CATEGORY_ID = 2
SPHERE_CATEGORY_ID = 3

freq_dict = {
    BACKGROUND_CATEGORY_ID: 0,
    CYLINDER_CATEGORY_ID: 0,
    CUBE_CATEGORY_ID: 0,
    SPHERE_CATEGORY_ID: 0
}

# Get all filenames for mask files in training set
filenames = get_all_image_files(dirs)

# For each file
for file in filenames:
    image = process_image(file, scaling_factor=1.0)

    unique, counts = np.unique(image, return_counts=True)
    for pixel_category, counts in zip(unique, counts):
        freq_dict[pixel_category] += counts

median = np.median(np.asarray([v for v in freq_dict.itervalues()]))

print(freq_dict)
for pixel_category in freq_dict.iterkeys():
    print(np.float(np.float(median) / freq_dict[pixel_category]))

print(median)
# Add count of occurrences in mask file to frequency
