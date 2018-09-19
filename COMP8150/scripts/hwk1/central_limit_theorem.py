import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binom, skew

np.random.seed(5)

# Binomial Distribution Parameters
n = 10
p = 0.2

# Descriptive Stats for Original Probability Distribution
pop_mean, pop_var = binom.stats(n, p, loc=0, moments='mv')
pop_std = binom.std(n, p)

print('Population Mean: ', pop_mean)
print('Population Variance: ', pop_var)

# Random samples
x = np.arange(0, n + 1)
pmf = binom(n, p).pmf(x)

# Sample statistics
mean_of_means = []
variances = []
skews = []

samp_sizes = [5, 10, 50, 100]
for i, samp_size in enumerate(samp_sizes, start=1):
    means = []
    for sample in range(10000):
        pts = binom.rvs(n, p, size=samp_size)
        means.append(np.mean(pts))

    # Calculate sample statistics
    mean_of_means.append(np.mean(means))
    variances.append(np.var(means))
    skews.append(skew(means))

    plt.subplot(2, 2, i)
    plt.title('Histogram of Binomial Sample Means\n(Sample Size per Mean: {})'.format(samp_size), size='large')
    plt.xlabel('$\overline{X}$', size='large')
    plt.ylabel('Frequency', size='large')

    plt.hist(means, bins=100, facecolor='purple', weights=np.ones_like(means) / len(means), density=False, alpha=0.35,
             edgecolor='black', linewidth=0.5)

plt.subplots_adjust(hspace=.7)
plt.subplots_adjust(wspace=.4)
plt.show()

plt.gcf().clear()

x = np.linspace(1, samp_sizes[-1])
line_1, = plt.plot(x, np.ones_like(x) * pop_mean, 'b--')

plt.title('Mean vs Sample Size ($n$)', size='large')
plt.xlabel('Sample Size ($n$)', size='large')
plt.ylabel('Mean', size='large')
line_2, = plt.plot(samp_sizes, mean_of_means, 'rx')
plt.legend([line_1, line_2], ['Expected Mean $\mu$', 'Calculated Mean'], loc='upper right')
plt.show()

plt.gcf().clear()

x = np.linspace(1, samp_sizes[-1])
line_1, = plt.plot(x, pop_var / np.array(x), 'b--')

plt.title('Variance vs Sample Size ($n$)', size='large')
plt.xlabel('Sample Size ($n$)', size='large')
plt.ylabel('Variance', size='large')
line_2, = plt.plot(samp_sizes, variances, 'rx')
plt.legend([line_1, line_2], ['Expected Variance $\sigma^2/n$', 'Calculated Variance'], loc='upper right')
plt.show()
plt.gcf().clear()

plt.title('Skew vs Sample Size ($n$)', size='large')
plt.xlabel('Sample Size ($n$)', size='large')
plt.ylabel('Skew', size='large')
plt.plot(samp_sizes, skews)
plt.show()
plt.gcf().clear()