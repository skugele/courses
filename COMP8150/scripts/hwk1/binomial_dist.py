import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binom

np.random.seed(1)

# Binomial Distribution
n = 10
p = 0.3

mean, var = binom.stats(n, p, loc=0, moments='mv')
std = binom.std(n, p)
x = np.arange(0, n + 1)
pmf = binom(n, p).pmf(x)

fig, ax = plt.subplots(1, 1)

ax.plot(x, pmf, 'b-', lw=3, alpha=0.6, label='bnom')

q1 = binom.ppf(.25, n, p)
median = binom.ppf(.5, n, p)
q3 = binom.ppf(.75, n, p)

plt.title('Binomial Distribution \n($\mu$: {}, $\sigma$: {}, $\sigma^2$: {})'.format(mean, std, var), size='xx-large')

plt.xlabel('X', size='large')
plt.ylabel('P(X)', size='large')

# Quartile lines
ax.axvline(x=q1, linewidth=3, alpha=0.6, color='red', linestyle='dashed')
ax.axvline(x=median, linewidth=3, alpha=0.6, color='red', linestyle='dashed')
ax.axvline(x=q3, linewidth=3, alpha=0.6, color='red', linestyle='dashed')

horiz_text_offset = 0.6
vert_text_offset = 0.1

plt.xlim(x[0], x[-1])
plt.text(x[0] + (q1 - x[0]) / 2.0 - horiz_text_offset, vert_text_offset, 'Q1', color='black', size='x-large')
plt.text(q1 + (median - q1) / 2.0 - horiz_text_offset, vert_text_offset, 'Q2', color='black', size='x-large')
plt.text(median + (q3 - median) / 2.0 - horiz_text_offset, vert_text_offset, 'Q3', color='black', size='x-large')
plt.text(q3 + (x[-1] - q3) / 2.0 - horiz_text_offset, vert_text_offset, 'Q4', color='black', size='x-large')

# Random samples
samp_size = 100
pts = binom.rvs(n, p, size=samp_size)

# Add histogram for sampled points
ys = [.005] * samp_size
plt.hist(pts, bins=7, facecolor='purple', alpha=0.45, weights=np.ones_like(pts) / float(len(pts)), density=False,
         edgecolor='black', linewidth=1.0)
plt.plot(pts, ys, 'bx')

plt.show()
