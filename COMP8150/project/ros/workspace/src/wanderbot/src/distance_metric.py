from image_util import *


def get_unique_rgbs_for_specs(specs):
    imgs = np.asarray([s.data for s in specs])
    rgbs, counts = np.unique(np.reshape(imgs, (-1, 3)), axis=0, return_counts=True)
    ndxs = np.asarray(list(reversed(np.argsort(counts))))
    rgbs = rgbs[ndxs]
    counts = counts[ndxs]
    prob = counts / np.double(np.sum(counts))

    return rgbs, counts, prob


def rgb_distance_from_cluster(rgbs, cmp_rgbs):
    s = np.float(0)

    for rgb in rgbs:
        l2_diff = np.asarray(map(np.linalg.norm, (rgb - cmp_rgbs)))
        closest_match = np.argmin(l2_diff)
        v = l2_diff[closest_match]
        s += v

    return s


image_specs = get_image_specs(images_dir, labels=get_categories(labels_file), scaling_factor=0.1)
category_specs = find_image_specs_by_category(image_specs, ['6'])

target_spec = find_image_specs_by_id(image_specs, ['50'])
target_rgb_values,_,_ = get_unique_rgbs_for_specs(target_spec)

cmp_rgbs, _, _ = get_unique_rgbs_for_specs(category_specs)

s = rgb_distance_from_cluster(target_rgb_values, cmp_rgbs[0:10])
print(s)
