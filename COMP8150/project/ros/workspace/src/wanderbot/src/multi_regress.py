import random

from matplotlib.colors import ColorConverter
from mpl_toolkits.mplot3d import Axes3D

from matplotlib.ticker import FuncFormatter

from image_util import *
from distance_metric import *
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from mpl_toolkits import mplot3d


# def luminosity(image):
#     rgb_values = np.reshape(image, (-1, 3))
#     scaled_rgb = rgb_values / np.float(255)
#     rgb_max = np.max(scaled_rgb)
#     rgb_min = np.min(scaled_rgb)
#
#     return rgb_max - rgb_min


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


random.seed(8675309)

image_specs = get_image_specs(images_dir, labels=get_categories(labels_file), scaling_factor=0.1)

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

# plt.scatter(x_2, y, c=cs)
# plt.xlabel(r'$x_2$ (Sum of RGB Euclidean Distances)')
# # plt.xlabel(r'$x_1$ (Average $L_{avg}$)')
# plt.ylabel(r'y')
# # plt.title(r'$x_1$  vs $y$')
# plt.colorbar(format=FuncFormatter(get_label))
# plt.savefig('/home/skugele/Development/courses/COMP8150/project/figures/MultiRegressDistVsCategory.png')
# # plt.savefig('/home/skugele/Development/courses/COMP8150/project/figures/MultiRegressLavgVsCategory.png')


# X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
# y = 1 * x_0 + 2 * x_1 + 3
# y = np.dot(X, np.array([1, 2])) + 3

X = np.column_stack((x_1, x_2))

reg = LinearRegression().fit(X, y)
# print('score: ' + str(reg.score(X, y)))

# print(reg.coef_)
# print(reg.intercept_)

# reg.predict(np.array([[3, 5]]))

# plot the surface
# plt3d = plt.figure().gca(projection='3d')
# plt3d.plot_surface(xx, yy, z, alpha=0.2)
#
# # Ensure that the next plot doesn't overwrite the first plot
# ax = plt.gca()
# ax.hold(True)
#
# ax.scatter(points2[0], point2[1], point2[2], color='green')

# plot plane

# x1_space = np.linspace(0, 50)
# x2_space = np.linspace(-1000, 10000)
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
# # ax.set_zlim(-0.2, 1.2)
#
# ax.set_xlabel(r'$x_1$')
# ax.set_ylabel(r'$x_2$')
# ax.set_zlabel(r'$y$')
# ax.set_title('Multi-Regression Hyper-Plane with Scatter Plot')
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
    print('{},{}'.format(str(y_pred),str(y_true)))
