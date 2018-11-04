import matplotlib.pyplot as plt

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

from matplotlib.ticker import FuncFormatter

from image_util import *


def apply_pca(data, categories, n_components, plot=False):
    pca = PCA(n_components)
    pca_result = pca.fit_transform(data)

    if plot:
        plt.scatter(pca_result[:, 0], pca_result[:, 1], c=categories, cmap=plt.cm.get_cmap('tab10', 6))
        plt.title('PCA dimensionality reduction applied to images')
        plt.xlabel('c1')
        plt.ylabel('c2')
        plt.colorbar(format=FuncFormatter(get_label))
        plt.show()

    return pca, pca_result


def apply_tsne(data, image_specs, n_components, plot=True):
    tsne = TSNE(n_components=n_components, perplexity=25, early_exaggeration=12,
                n_iter_without_progress=300, n_iter=10000, random_state=131, verbose=1)
    tsne_results = tsne.fit_transform(data)

    if plot:
        categories = [spec.category for spec in image_specs]
        ids = [spec.id for spec in image_specs]

        fig, ax = plt.subplots()
        plt.scatter(tsne_results[:, 0], tsne_results[:, 1], c=categories,
                    cmap=plt.cm.get_cmap('tab10', 6))
        plt.title('T-SNE dimensionality Reduction Applied to Sampled Images')
        plt.xlabel('Component 1')
        plt.ylabel('Component 2')
        plt.colorbar(format=FuncFormatter(get_label))

        # for i, txt in enumerate(ids):
        #     ax.annotate(txt, (tsne_results[i, 0], tsne_results[i, 1]))

        plt.show()

    return tsne, tsne_results


image_specs = get_image_specs(images_dir, labels=get_categories(labels_file), scaling_factor=0.1)

images = np.asarray([spec.data for spec in image_specs])

pca, pca_result = apply_pca(images, image_specs, n_components=50, plot=False)

print 'Cumulative explained variation: {}'.format(np.sum(pca.explained_variance_ratio_))

tsne, tsne_result = apply_tsne(pca_result, image_specs, n_components=2, plot=True)

print 'KL divergence: {}'.format(tsne.kl_divergence_)
