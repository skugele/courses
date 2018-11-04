import os
import re
import cv2
import numpy as np
import operator as ops
import collections

images_dir = '/var/local/data/skugele/COMP8150/project/images'
labels_file = '/var/local/data/skugele/COMP8150/project/images/labels'

object_labels = [i for i in range(1, 5)]
multi_object_label = 5
no_object_label = 6


def get_categories(labels_file):
    labels = {}
    with open(labels_file, 'r') as fp:
        line = fp.readline()
        while line:
            id, label = line.strip().split(',')
            labels[id] = label
            line = fp.readline()
    return labels


def get_label(category):
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
    img_match_regex = re.compile('image_(\d+).png$')

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
