import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

np.random.seed(5)

# Normal Distribution
mean, var = norm.stats(moments='mv')
std = norm.std()

fig, ax = plt.subplots(1, 1)

x = np.linspace(norm.ppf(0.05), norm.ppf(0.95))
ax.plot(x, norm.pdf(x), 'b-', lw=3, alpha=0.6, label='Gaussian')

q1 = norm.ppf(.25)
median = norm.ppf(.5)
q3 = norm.ppf(.75)

plt.title('Gaussian Distribution ($\mu$: {:.2f}, $\sigma$: {:.2f}, $\sigma^2$: {:.2f})'.format(mean, std, var),
          size='xx-large')
plt.xlabel('X', size='large')
plt.ylabel('P(X)', size='large')

# Quartile lines
ax.axvline(x=q1, linewidth=3, alpha=0.6, color='black', linestyle='dashed')
ax.axvline(x=median, linewidth=3, alpha=0.6, color='black', linestyle='dashed')
ax.axvline(x=q3, linewidth=3, alpha=0.6, color='black', linestyle='dashed')

horiz_text_offset = .1
vert_text_offset = 0.25

plt.xlim(x[0], x[-1])
plt.text(x[0] + (q1 - x[0]) / 2.0 - horiz_text_offset, vert_text_offset, 'Q1', color='black', size='xx-large')
plt.text(q1 + (median - q1) / 2.0 - horiz_text_offset, vert_text_offset, 'Q2', color='black', size='xx-large')
plt.text(median + (q3 - median) / 2.0 - horiz_text_offset, vert_text_offset, 'Q3', color='black', size='xx-large')
plt.text(q3 + (x[-1] - q3) / 2.0 - horiz_text_offset, vert_text_offset, 'Q4', color='black', size='xx-large')

# Random samples
samp_size = 100
pts = norm.rvs(size=samp_size)

# Add histogram

ys = [.005] * samp_size
plt.hist(pts, bins=20, facecolor='purple', alpha=0.45, density=True, weights=np.ones_like(pts) / float(len(pts)),
         edgecolor='black',
         linewidth=1.0)
plt.plot(pts, ys, 'bx')

plt.show()

# Sample statistics
std_sample = np.std(pts)
var_sample = np.var(pts)
mean_sample = np.mean(pts)
q1_sample, median_sample, q3_sample = np.percentile(pts, [25, 50, 75])

print('mean: {:.2f}, mean(sample): {:.2f}'.format(mean, mean_sample))
print('var: {:.2f}, var(sample): {:.2f}'.format(var, var_sample))
print('std: {:.2f}, std(sample): {:.2f}'.format(std, std_sample))

print('q1: {:.2f}, q1(sample): {:.2f}'.format(q1, q1_sample))
print('median: {:.2f}, median(sample): {:.2f}'.format(median, median_sample))
print('q3: {:.2f}, q3(sample): {:.2f}'.format(q3, q3_sample))
