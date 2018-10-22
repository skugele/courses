README: Programming Assignment 2 (10/21/2018)
Author: Sean Kugele (skugele@memphis.edu - U00184373)

Prerequisites: Python 3

An anaconda script (conda/env.yml) has been provided to create an environment identical to the development environment; however, any version of Python 3 interpreter should be sufficient.

Script Location: scripts/pa2.py
Usage: "python scripts/pa2.py"
Example Execution:

  $ python scripts/pa2.py

    Specify a graph. (A blank line stops input)
    5
    1,2
    3,4
    3,1

    YES
    5 3 4 1 2
    1

Code Structure:
---------------

scripts/

  graph.py -- Contains primary functions such as "is_dag", "topological_sort", and "find_longest_path_distance"
  pa2.py   -- Driver script

conda/

  env.yml -- anaconda environment script ('conda env create -f env.yml' can be used to retrieve all dependencies using Anaconda)




