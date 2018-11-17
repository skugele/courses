import os
import re
import cv2
import numpy as np
import operator as ops
import collections

images_dir = '/var/local/data/skugele/COMP8150/project/images'
labels_file = '/var/local/data/skugele/COMP8150/project/images/labels'

synthetic_images_dir = '/var/local/data/skugele/COMP8150/project/synthetic_images'

object_labels = [i for i in range(1, 5)]
multi_object_label = 5
no_object_label = 6

# OpenCv processes images as BGR
RED_POS = 2
GREEN_POS = 1
BLUE_POS = 0


def get_categories(labels_file):
    labels = {}
    with open(labels_file, 'r') as fp:
        line = fp.readline()
        while line:
            id, label = line.strip().split(',')
            labels[id] = label
            line = fp.readline()
    return labels


def get_label(category, pos=None):
    if category in object_labels:
        return 'object {}'.format(int(category))
    elif category == multi_object_label:
        return 'multiple objects'
    else:
        return 'no objects'


ImageSpec = collections.namedtuple('ImageSpec', ['id', 'filename', 'category', 'data'])


def process_image(filename, scaling_factor):
    raw_image = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    scaled_image = cv2.resize(raw_image, None, fx=scaling_factor, fy=scaling_factor)
    flattened_img = np.reshape(scaled_image, newshape=(reduce(ops.mul, scaled_image.shape, 1)))

    return flattened_img


def get_image_specs(images_dir, labels, scaling_factor):
    img_match_regex = re.compile('image_([1-9]\d+).png$')

    image_specs = []
    for root, _, files in os.walk(images_dir):
        files = filter(lambda f: img_match_regex.match(f), files)
        for file in files:
            found = img_match_regex.search(file)
            if found:
                id = found.group(1)
                filename = '/'.join([root, file])
                category = labels[id]
                data = process_image(filename, scaling_factor)

                spec = ImageSpec(id, filename, category, data)
                image_specs.append(spec)

    return sorted(image_specs, cmp=lambda x, y: int(x.id) - int(y.id))


def find_image_specs_by_id(image_specs, ids):
    return filter(lambda s: s.id in ids, image_specs)


def find_image_specs_by_category(image_specs, categories):
    return filter(lambda s: s.category in categories, image_specs)


def get_rgb_values(imgs):
    rgb_values = []
    colors = []

    for color in range(3):
        imgs = np.copy(imgs)

        rgb_values.append(np.reshape(np.asarray(imgs[:, color::3]), (-1)))
        colors.append(color)

    return rgb_values, colors


def rel_luminance(r, g, b):
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def calc_l_avg(spec):
    rgb_values = np.reshape(spec.data, (-1, 3))

    r_vals = rgb_values[:, RED_POS]
    b_vals = rgb_values[:, BLUE_POS]
    g_vals = rgb_values[:, GREEN_POS]

    return (np.average(rel_luminance(r_vals, g_vals, b_vals)))


def calc_avg_l_avgs(image_specs):
    avg_l_avgs = {}
    for c in map(str, range(1, 7)):
        avg_l_avgs[c] = np.average([calc_l_avg(spec) for spec in find_image_specs_by_category(image_specs, c)])

    return avg_l_avgs
