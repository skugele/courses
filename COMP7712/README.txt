README: Programming Assignment 1 (10/9/2018)
Author: Sean Kugele (skugele@memphis.edu - U00184373)

Prerequisites: Python 3

An anaconda script (conda/env.yml) has been provided to create an environment identical to the development environment; however, any version of Python 3 interpreter should be sufficient.

###############################
# Part 1: Polynomial Division #
###############################
Script Location: scripts/pa1_1.py
Usage: "python scripts/pa1_1.py"
Example Execution:

  $ python scripts/pa1_1.py 
  Please specify a polynomial: 3 5 1 10 0 5
  Please provide a number: 1
  Results of dividing (5.0x^3 + 10.0x + 5.0) by (x - 1.0) is

  Quotient: 5.0x^2 + 5.0x + 15.0
  Remainder: 20.0

#####################################
# Part 2: Polynomial Multiplication #
#####################################
Script Location: scripts/pa1_2.py
Usage: "python scripts/pa1_2.py"
Example Execution:

  $ python scripts/pa1_2.py 
  Please specify a list of numbers: 1 2 -2 -1 7 8.5 
  Computing:  (x - 1.0)(x - 2.0)(x + 2.0)(x + 1.0)(x - 7.0)(x - 8.5)
  Result:  x^6 - 15.5x^5 + 54.5x^4 + 77.5x^3 - 293.5x^2 - 62.0x + 238.0

####################################
# Part 3: Polynomial Interpolation #
####################################
Script Location: scripts/pa1_3.py
Usage: "python scripts/pa1_3.py"
Example Execution:

  $ python scripts/pa1_3.py 
  Please specify a set of points: -1 -1 0 0 1 1 2 8
  Interpolating over points: {(-1.0, -1.0),(0.0, 0.0),(1.0, 1.0),(2.0, 8.0)}
  Result:  x^3


Code Structure:
---------------

scripts/

  functions.py  -- Contains primary functions such as "poly_divide", "poly_multiply", and "interpolate"
  polynomial.py -- Contains a supporting class for basic polynomial representation and manipulation
  pa1_1.py      -- Driver script for part (1)
  pa1_2.py      -- Driver script for part (2)
  pa1_3.py      -- Driver script for part (3)
  
conda/

  env.yml -- anaconda environment script ('conda env create -f env.yml' can be used to retrieve all dependencies using Anaconda)




