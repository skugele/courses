from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

from image_util import *

image_specs = get_image_specs(images_dir, labels=get_categories(labels_file), scaling_factor=0.1)
images_for_object = {c: [] for c in map(str, range(1, 7))}

for c in images_for_object.keys():
    images_for_object[c] = np.asarray([spec.data for spec in filter(lambda s: s.category == c, image_specs)])

specs = find_image_specs_by_id(image_specs, ['2'])
rgb_values, colors = get_rgb_values(np.asarray([s.data for s in image_specs]))

xs = rgb_values[0]
ys = rgb_values[1]
zs = rgb_values[2]

plt.scatter(xs, ys)
plt.xlabel('Blue')
plt.ylabel('Green')
plt.show()
plt.close()

plt.scatter(ys, zs)
plt.xlabel('Green')
plt.ylabel('Red')
plt.show()
plt.close()

plt.scatter(xs, zs)
plt.xlabel('Blue')
plt.ylabel('Red')
plt.show()
plt.close()


plt.show()