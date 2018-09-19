import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binom, skew, kurtosis

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

# Sample statistics
skews = []
kurtoses = []


samp_sizes = [5,10,50,100]
for i, samp_size in enumerate(samp_sizes, start=1):
    means = []
    for sample in range(10000):
        pts = binom.rvs(n, p, size=samp_size)
        means.append(np.mean(pts))

    # Calculate sample statistics
    skews.append(abs(skew(means)))
    kurtoses.append(abs(kurtosis(means)))

    plt.subplot(2, 2, i)
    plt.title('Histogram of Binomial Sample Means\n(Sample Size per Mean: {})'.format(samp_size), size='large')
    plt.xlabel('X', size='large')
    plt.ylabel('$\mathcal{N}(X)$', size='large')

    plt.hist(means, bins=100, facecolor='purple', weights = np.ones_like(means)/len(means), density=False, alpha=0.35, edgecolor='black', linewidth=0.5)

plt.subplots_adjust(hspace=.7)
plt.subplots_adjust(wspace=.4)
plt.show()

plt.gcf().clear()

plt.title('Skew As A Function Of Sample Size $N$', size='large')
plt.xlabel('Sample Size ($N$)', size='large')
plt.ylabel('Skew', size='large')
plt.plot(samp_sizes, skews)
plt.show()
plt.gcf().clear()

plt.title('Kurtosis As A Function Of Sample Size $N$', size='large')
plt.xlabel('Sample Size ($N$)', size='large')
plt.ylabel('Kurtosis', size='large')
plt.plot(samp_sizes, kurtoses)
plt.show()
plt.gcf().clear()

