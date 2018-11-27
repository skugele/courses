from sklearn.cluster import KMeans
import numpy as np
import cv2

from image_util import images_dir, get_image_specs, get_categories, labels_file, find_image_specs_by_id, get_rgb_values

n_clusters = 6
scaling_factor = .25
dims = 480, 640
scaled_dims = map(lambda dim: int(dim * scaling_factor), dims)

image_specs = get_image_specs(images_dir, labels=get_categories(labels_file), scaling_factor=scaling_factor)
spec = find_image_specs_by_id(image_specs, ['47'])[0]

image = np.reshape(spec.data, newshape=(scaled_dims[0], scaled_dims[1], -1))
rgbs = np.reshape(spec.data, newshape=(-1, 3))

# cv2.imshow('image', image)
# cv2.imwrite('/tmp/original.png', image)
# cv2.waitKey()

colors = [[50, 50, 50],  # Gray
          [200, 200, 50],  # Cyan
          [200, 50, 50],  # Purple
          [30, 30, 200],  # Pale Red
          [20, 200, 50],  # Green
          [20, 150, 200],  # Yellow
          ]

# print(np.asarray(images).shape)
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(rgbs)
# print(type(kmeans.labels_))
print(kmeans.cluster_centers_)
print('Inertia: ' + str(kmeans.inertia_))

for c in range(n_clusters):
    rgbs[kmeans.labels_ == c] = np.asarray(colors[c])

clustered_image = np.reshape(rgbs, newshape=(scaled_dims[0], scaled_dims[1], -1))
# cv2.imshow('clustering', clustered_image)
# cv2.waitKey()
# cv2.imwrite('/tmp/coloring{}.png'.format(n_clusters), image)

# kmeans.predict([[0, 0], [4, 4]])
