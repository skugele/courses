import os
import re
import cv2
import numpy as np
import matplotlib.pyplot as plt
import operator as ops
import collections

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

images_dir = '/var/local/data/skugele/COMP8150/project/images'
labels_file = '/var/local/data/skugele/COMP8150/project/images/labels'


def get_labels(labels_file):
    labels = {}
    with open(labels_file, 'r') as fp:
        line = fp.readline()
        while line:
            id, label = line.strip().split(',')
            labels[id] = label
            line = fp.readline()
    return labels


ImageSpec = collections.namedtuple('ImageSpec', ['id', 'filename', 'label', 'data'])


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
                label = labels[id]
                data = process_image(filename, scaling_factor)

                spec = ImageSpec(id, filename, label, data)
                image_specs.append(spec)

    return sorted(image_specs, cmp=lambda x, y: int(x.id) - int(y.id))


def apply_pca(data, labels, n_components, plot=True):
    pca = PCA(n_components)
    pca_result = pca.fit_transform(data)

    if plot:
        plt.scatter(pca_result[:, 0], pca_result[:, 1], c=labels, cmap=plt.cm.get_cmap('tab10', 6))
        plt.title('PCA dimensionality reduction applied to images')
        plt.xlabel('c1')
        plt.ylabel('c2')
        plt.colorbar()
        plt.show()

    return (pca, pca_result)


def apply_tsne(data, labels, n_components, perplexity, n_iter, plot=True):
    tsne = TSNE(n_components, perplexity, n_iter, verbose=1)
    tsne_results = tsne.fit_transform(data)

    if plot:
        plt.scatter(tsne_results[:, 0], tsne_results[:, 1], c=labels, cmap=plt.cm.get_cmap('tab10', 6))
        plt.title('T-SNE dimensionality reduction applied to images')
        plt.xlabel('c1')
        plt.ylabel('c2')
        plt.colorbar()
        plt.show()

    return (tsne, tsne_results)


image_specs = get_image_specs(images_dir, labels=get_labels(labels_file), scaling_factor=0.1)

data = np.asarray([spec.data for spec in image_specs])
labels = [spec.label for spec in image_specs]

pca, pca_result = apply_pca(data, labels, n_components=25, plot=True)

print 'Cumulative explained variation: {}'.format(np.sum(pca.explained_variance_ratio_))

tsne, tsne_result = apply_tsne(data, labels, n_components=2, perplexity=40, n_iter=300, plot=True)
