from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from matplotlib.colors import Normalize

import matplotlib.cm as cmx

import numpy as np
import cv2

from image_util import *

image_specs = get_image_specs(images_dir, labels=get_categories(labels_file), scaling_factor=0.1)
images_for_object = {c: [] for c in map(str, range(1, 7))}

for c in images_for_object.keys():
    images_for_object[c] = np.asarray([spec.data for spec in filter(lambda s: s.category == c, image_specs)])

specs = find_image_specs_by_category(image_specs, ['1', '2', '3', '4', '5', '6'])
# specs = find_image_specs_by_id(image_specs, ['50'])
# specs = image_specs
imgs = np.asarray([s.data for s in specs])
rgb_values = np.reshape(imgs, (-1, 3))
uniq_rgb_values, uniq_counts = np.unique(rgb_values, axis=0, return_counts=True)
sorted_order_indices = np.asarray(list(reversed(np.argsort(uniq_counts))))

uniq_rgb_values = uniq_rgb_values[sorted_order_indices]
uniq_counts = uniq_counts[sorted_order_indices]

total_values = np.sum(uniq_counts)
prob = uniq_counts / np.double(np.sum(uniq_counts))

# indices = np.random.choice(np.arange(0, len(prob)), size=(640 * 480), p=prob)
# chosen_rgb = uniq_rgb_values[indices]

# img = np.reshape(chosen_rgb, (480,640,3))
# img_sorted = np.sort(img, axis=2)
# cv2.imshow("image", img_sorted)
# cv2.waitKey()



# ax = fig.add_subplot(111, projection='3d')

xs = uniq_rgb_values[:, 0]
ys = uniq_rgb_values[:, 1]
zs = uniq_rgb_values[:, 2]

cm = plt.get_cmap('jet')
c_norm = Normalize(vmin=min(prob), vmax=max(prob))
scalar_map = cmx.ScalarMappable(norm=c_norm, cmap=cm)
fig = plt.figure()
ax=Axes3D(fig)
scalar_map.set_array(prob)
# ax.scatter(xs, ys, zs, c=prob, cmap=plt.cm.get_cmap('Accent'))
ax.scatter(xs, ys, zs, s=prob*15000, c=scalar_map.to_rgba(prob), alpha=0.6, cmap=cm)

fig.colorbar(scalar_map)

ax.set_xlabel('Blue')
ax.set_ylabel('Green')
ax.set_zlabel('Red')

plt.show()
# plt.savefig(pad_inches=0.2, fname='/home/skugele/Development/courses/COMP8150/project/figures/No Objects Category 3D Probability Scatter Plot.png')
# #

#
#
# # print(np.argmax(uniq_counts))
#
# # def rgb_distance(v1, v2):
# # return np.linalg.norm(v1-v2)
#
#
# # np.asarray(imgs[:, color::3])
#
#
# # rgb_values = []
# # colors = []
# #
# # for color in range(3):
# #     imgs = np.copy(imgs)
# #
# #     rgb_values.append(np.reshape(np.asarray(imgs[:, color::3]), (-1)))
# #     colors.append(color)
