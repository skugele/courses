from image_util import *

import numpy as np
import matplotlib.pyplot as plt
import cv2

image_specs = get_image_specs(images_dir, labels=get_categories(labels_file), scaling_factor=0.1)
images = np.asarray([spec.data for spec in image_specs])

images_for_object = {c: [] for c in map(str, range(1, 7))}

for c in images_for_object.keys():
    images_for_object[c] = np.asarray([spec.data for spec in filter(lambda s: s.category == c, image_specs)])


def get_facecolor(v):
    return ['b', 'g', 'r'][v]


def get_color_name(v):
    return ['Blue', 'Green', 'Red'][v]


def get_rgb_values(imgs):
    rgb_values = []
    colors = []

    for color in range(3):
        imgs = np.copy(imgs)

        rgb_values.append(np.reshape(np.asarray(imgs[:, color::3]), (-1)))
        colors.append(color)

    return rgb_values, colors


def create_rgb_histogram(ax, rgb_values, colors, category):
    ax.set_xlim([0, 255])
    ax.set_ylim([0, 350])
    #
    # ax[r, c].set_xlabel('RGB pixel value (0-255)')
    ax.set_ylabel('# pixels with RGB value')
    ax.set_title('Histogram for \"{}\" RGB-D images'.format(get_label(int(category))))
    ax.grid(True)
    ax.hist(rgb_values, bins=64, density=False, color=map(lambda c: get_facecolor(c), colors),
            weights=[np.ones_like(x) for x in rgb_values], label=map(lambda c: get_color_name(c), colors))
    ax.legend(loc='upper right')
    # ax.text(15, 300, get_label(int(category)), style='italic', fontsize=16, bbox={'facecolor': 'w'})


def create_rgb_histgrams_for_all_categories():
    n_rows = 3
    n_cols = 2

    fig, ax = plt.subplots(n_rows, n_cols)

    for r in range(n_rows):
        for c in range(n_cols):
            category = str(c + n_cols * r + 1)
            imgs = np.copy(images_for_object[category])
            rgb_values, colors = get_rgb_values(imgs)

            create_rgb_histogram(ax[r, c], rgb_values, colors, category)

    fig.subplots_adjust(wspace=0.2, hspace=0.35)
    plt.show()
    plt.close()


def create_histogram_from_image_spec(spec):
    fix, ax = plt.subplot()

    rgb_values, colors = get_rgb_values(spec.data)
    create_rgb_histogram(ax, rgb_values, colors, spec.category)

    plt.show()
    plt.close()


spec = image_specs