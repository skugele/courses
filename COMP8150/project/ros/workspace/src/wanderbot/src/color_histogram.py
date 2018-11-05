from image_util import *

import numpy as np
import matplotlib.pyplot as plt

image_specs = get_image_specs(images_dir, labels=get_categories(labels_file), scaling_factor=0.1)
images_for_object = {c: [] for c in map(str, range(1, 7))}

for c in images_for_object.keys():
    images_for_object[c] = np.asarray([spec.data for spec in filter(lambda s: s.category == c, image_specs)])


def get_facecolor(v):
    return ['b', 'g', 'r'][v]


def get_color_name(v):
    return ['Blue', 'Green', 'Red'][v]


def create_rgb_histogram(ax, rgb_values, colors):
    ax.set_xlim([0, 255])
    #
    ax.set_xlabel('RGB pixel value (0-255)')
    ax.set_ylabel('Proportion of pixels with value')

    ax.grid(True)
    ax.hist(rgb_values, bins=256, density=False,
            weights=[np.ones_like(x) / float(len(x)) for x in rgb_values],
            color=map(lambda c: get_facecolor(c), colors),
            label=map(lambda c: get_color_name(c), colors))
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

            create_rgb_histogram(ax[r, c], rgb_values, colors)
            ax[r, c].set_title('\"{}\" RGB-D images'.format(get_label(int(category))))

    fig.subplots_adjust(wspace=0.2, hspace=0.6)
    plt.show()
    plt.close()


def create_histogram_from_image_specs(specs, title):
    fix, ax = plt.subplots()

    rgb_values, colors = get_rgb_values(np.asarray([s.data for s in specs]))
    create_rgb_histogram(ax, rgb_values, colors)
    ax.set_title(title)

    plt.show()
    plt.close()


# create_rgb_histgrams_for_all_categories()

specs = find_image_specs_by_id(image_specs, ['50'])
create_histogram_from_image_specs(specs, 'Histogram of RGB values from single "object 1" image')
