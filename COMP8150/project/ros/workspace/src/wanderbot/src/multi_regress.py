import random

from matplotlib.ticker import FuncFormatter

from image_util import *
import matplotlib.pyplot as plt


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

# Hold out 50 images for testing
# for spec in image_specs[0:250]:
#     cs.append(int(spec.category))
#     y.append(1 if spec.category == '6' else 0)
#     x_1.append(np.abs(calc_l_avg(spec) - avg_l_avgs['6']))
#     x_2.append(...)
#     # print('[category: {}, id: {}, x_1: {} x_2: {} y:{}'.format(spec.category, spec.id, x_1[-1], x_2[-1], y[-1]))

# plt.scatter(x_1, y, c=cs)
# plt.xlabel(r'$x_1$')
# plt.ylabel('y')
# plt.title(r'Image Category vs Average $L_{avg}$')
# plt.colorbar(format=FuncFormatter(get_label))
# plt.savefig('/home/skugele/Development/courses/COMP8150/project/figures/MultiRegressLavgVsCategory.png')
