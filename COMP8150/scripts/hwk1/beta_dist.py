import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import beta

np.random.seed(1)

# Beta Distribution
a, b = 3.0, 2.0
mean, var = beta.stats(a, b, moments='mv')
std = beta.std(a, b, loc=0, scale=1)

fig, ax = plt.subplots(1, 1)

x = np.linspace(beta.ppf(0.05, a, b), beta.ppf(0.95, a, b))
ax.plot(x, beta.pdf(x, a, b), 'b-', lw=3, alpha=0.6, label='Beta')

q1 = beta.ppf(.25, a, b)
median = beta.ppf(.5, a, b)
q3 = beta.ppf(.75, a, b)

plt.title('Beta Distribution ($\mu$: {}, $\sigma$: {}, $\sigma^2$: {})'.format(mean, std, var), size='xx-large')
plt.xlabel('X', size='large')
plt.ylabel('P(X)', size='large')

# Quartile lines
ax.axvline(x=q1, linewidth=3, alpha=0.6, color='black', linestyle='dashed')
ax.axvline(x=median, linewidth=3, alpha=0.6, color='black', linestyle='dashed')
ax.axvline(x=q3, linewidth=3, alpha=0.6, color='black', linestyle='dashed')

horiz_text_offset = .01
vert_text_offset = 0.5

plt.xlim(x[0], x[-1])
plt.text(x[0] + (q1 - x[0]) / 2.0 - horiz_text_offset, vert_text_offset, 'Q1', color='black', size='xx-large')
plt.text(q1 + (median - q1) / 2.0 - horiz_text_offset, vert_text_offset, 'Q2', color='black', size='xx-large')
plt.text(median + (q3 - median) / 2.0 - horiz_text_offset, vert_text_offset, 'Q3', color='black', size='xx-large')
plt.text(q3 + (x[-1] - q3) / 2.0 - horiz_text_offset, vert_text_offset, 'Q4', color='black', size='xx-large')

# Random samples
samp_size = 100
pts = beta.rvs(a, b, size=samp_size)

# Add histogram

ys = [.005] * samp_size
plt.hist(pts, facecolor='purple', alpha=0.45, weights=np.ones_like(pts) / float(len(pts)), density=True,
         edgecolor='black', linewidth=1.0)
plt.plot(pts, ys, 'bx')

plt.show()

# Sample statistics
std_sample = np.std(pts)
var_sample = np.var(pts)
mean_sample = np.mean(pts)
q1_sample, median_sample, q3_sample = np.percentile(pts, [25, 50, 75])

print('mean: {}, mean(sample): {}'.format(mean, mean_sample))
print('var: {}, var(sample): {}'.format(var, var_sample))
print('std: {}, std(sample): {}'.format(std, std_sample))

print('q1: {}, q1(sample): {}'.format(q1, q1_sample))
print('median: {}, median(sample): {}'.format(median, median_sample))
print('q3: {}, q3(sample): {}'.format(q3, q3_sample))
