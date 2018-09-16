#! /usr/bin/env python

import pandas as pd
import numpy as np
from random import random

# global parameters
learn_rate = 0.1
n_epochs = 500


# perceptron threshold function
def sgn(z):
    if z > 0:
        return 1
    else:
        return -1


# import data set
df = pd.read_csv('../data/hw1/d-10.csv')
n_rows, n_cols = df.shape

# randomly initialize weights + bias
weights = np.array([random() for w in range(n_cols)])

for epoch in xrange(n_epochs):

    errors = 0
    for i, row in df.iterrows():

        # appending additional input with value (1.0) for bias
        xs = np.append(row.values[:-1], 1.0)

        # classification label for training example
        cls = row.values[-1]

        # summation for linear unit
        z = np.dot(weights, xs)

        # output from perceptron
        out = sgn(z)

        # Check for misclassification and increment errors
        if cls != out:
            errors += 1

        delta = learn_rate * (cls - out) * xs

        # update weights
        weights += delta

    # Display summary
    print("epoch {}: {} errors".format(epoch, errors))



