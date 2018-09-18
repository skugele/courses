import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binom

np.random.seed(1)

# Binomial Distribution Parameters
n = 10
p = 0.1

# Descriptive Stats for Original Probability Distribution
pop_mean, pop_var = binom.stats(n, p, loc=0, moments='mv')
pop_std = binom.std(n, p)


# Random samples
x = np.arange(0, n + 1)
pmf = binom(n, p).pmf(x)

samp_sizes = [5,10,50,100]
for i, samp_size in enumerate(samp_sizes, start=1):
    means = []
    for sample in range(10000):
        pts = binom.rvs(n, p, size=samp_size)
        means.append(np.mean(pts))

    plt.subplot(2, 2, i)
    plt.title('Histogram of Binomial Sample Means\n(Sample Size per Mean: {})'.format(samp_size), size='large')
    plt.xlabel('X', size='large')
    plt.ylabel('$\mathcal{N}(X)$', size='large')

    plt.hist(means, bins=100, facecolor='purple', weights = np.ones_like(means)/len(means), density=False, alpha=0.35, edgecolor='black', linewidth=0.5)

plt.subplots_adjust(hspace=.7)
plt.subplots_adjust(wspace=.4)
plt.show()

# # Sample statistics
# skew = skew(means)
# kurtosis = kurtosis(np.ndarray(means))

# plt.hist(means, bins=100, facecolor='purple', alpha=0.35, density=False, edgecolor='black', linewidth=0.5)


#
#
#
# # Add histogram for sampled points
# ys = [.005] * samp_size

# plt.plot(pts, ys, 'bx')



# Normal Distribution
# mean, var = norm.stats(moments='mv', mean=10)
# std = norm.std()
#
# x = np.linspace(norm.ppf(0.05), norm.ppf(0.95))
# plt.plot(x, norm.pdf(x), 'b-', lw=3, alpha=0.6, label='Gaussian')
#
# plt.show()
#

