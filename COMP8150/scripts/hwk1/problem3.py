from scipy.stats import beta, norm, bernoulli, hypergeom
import matplotlib.pyplot as plt
import numpy as np


# Beta Distribution
a, b = 1.0, 1.0
mean, var = beta.stats(a, b, moments='mv')
std = beta.std(a, b, loc=0, scale=1)

# Normal Distribution
mean, var = norm.stats(moments='mv')
std = norm.std()

# Bernoulli Distribution
p = 0.3
mean, var = bernoulli.stats(p, moments='mv')
std = bernoulli.std(p)

# Hypergeometric Distribution
M, n, N = 20, 7, 12
mean, var = hypergeom.stats(M, n, N, loc=0, moments='mv')
std = hypergeom.std(M, n, N)