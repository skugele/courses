import random
from matplotlib.colors import ColorConverter

from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression

from image_util import *
from distance_metric import *

import matplotlib.pyplot as plt


def get_synthetic_image_specs(images_dir, scaling_factor=1.0):
    img_match_regex = re.compile('synthetic_(\d+).png$')

    n = 1
    image_specs = []
    for root, _, files in os.walk(images_dir):
        files = filter(lambda f: img_match_regex.match(f), files)
        for file in files:
            found = img_match_regex.search(file)
            if found:
                id = str(n)
                filename = '/'.join([root, file])
                category = root.split('/')[-1]
                data = process_image(filename, scaling_factor)

                spec = ImageSpec(id, filename, category, data)
                image_specs.append(spec)
                n += 1

    return sorted(image_specs, cmp=lambda x, y: int(x.id) - int(y.id))


random.seed(8675309)

image_specs = get_synthetic_image_specs(synthetic_images_dir, scaling_factor=0.1)

# Randomly shuffle the ordering in place for later selection
random.shuffle(image_specs)

avg_l_avgs = calc_avg_l_avgs(image_specs)

cs = []
y = []
x_1 = []
x_2 = []

cmp_rgbs, _, _ = get_unique_rgbs_for_specs(find_image_specs_by_category(image_specs, ['6']))
cmp_rgbs = cmp_rgbs[0:20]

# Hold out 50 images for testing
for spec in image_specs[0:250]:
    cs.append(int(spec.category))
    y.append(1 if spec.category == '6' else 0)
    x_1.append(np.abs(calc_l_avg(spec) - avg_l_avgs['6']))

    rgbs, _, _ = get_unique_rgbs_for_specs([spec])
    x_2.append(rgb_distance_from_cluster(rgbs, cmp_rgbs))
    # print('[category: {}, id: {}, x_1: {} x_2: {} y:{}'.format(spec.category, spec.id, x_1[-1], x_2[-1], y[-1]))


X = np.column_stack((x_1, x_2))

reg = LinearRegression().fit(X, y)
print('score: ' + str(reg.score(X, y)))

print(reg.coef_)
print(reg.intercept_)

# x1_space = np.linspace(0, 50)
# x2_space = np.linspace(-1000, 50000)
#
#
# def linear_model(reg, x1, x2):
#     return reg.intercept_ + x1 * reg.coef_[0] + x2 * reg.coef_[1]
#
#
# X, Y = np.meshgrid(x1_space, x2_space)
# Z = linear_model(reg, X, Y)
#
# fig = plt.figure()
# ax = Axes3D(fig)
#
# ax.set_xlabel(r'$x_1$')
# ax.set_ylabel(r'$x_2$')
# ax.set_zlabel(r'$y$')
# ax.set_title('Multi-Regression Hyper-Plane for Synthetic Data with Scatter Plot')
#
# ax.plot_surface(X, Y, Z, rstride=5, cstride=5, cmap='Blues', edgecolor=ColorConverter().to_rgba('black', alpha=0.4), alpha=0.4)
# ax.scatter(x_1, x_2, y, c=cs)
#
# plt.show()

cs = []
y = []
x_1 = []
x_2 = []

for spec in image_specs[250:-1]:
    cs.append(int(spec.category))
    y.append(1 if spec.category == '6' else 0)
    x_1.append(np.abs(calc_l_avg(spec) - avg_l_avgs['6']))

    rgbs, _, _ = get_unique_rgbs_for_specs([spec])
    x_2.append(rgb_distance_from_cluster(rgbs, cmp_rgbs))

X = np.column_stack((x_1, x_2))
pred = reg.predict(X)

for y_true, y_pred in zip(y, pred):
    print('{},{}'.format(str(y_pred), str(y_true)))
