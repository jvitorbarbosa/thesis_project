from base import compress_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# f = 2
# r = f * k /N
#
# N=5
#     DD               DC
# |———-----|——-----|----———|
# 0	      0,8	  1,2     1,6
#
# N=6
#     DD               DC
# |———-----|——-----|----———|
# 0	     0,67	   1	  1,67
#
# N=7
#     DD               DC
# |———-----|——-----|----———|
# 0		 0,85    1,14     1,71
#
# N=8
#     DD               DC
# |———-----|——-----|----———|
# 0	     0,75      1      1,75

def calculate_coefficient(n):
    f = 2
    idiv = math.ceil(n/2)
    print("[{}] division is {}".format(n, idiv))
    top = (n-1)*f/n
    bottom = 0
    l1 = (idiv-1)*f/n
    l2 = (idiv)*f/n
    # print("{}, {}, {}, {}".format(bottom, l1, l2, top))
    return (top-l2)/(l1-bottom)

def main():
    labels = [str(i) for i in range(3, 11)]
    major_data = []

    for n in labels:
        major_data.append(compress_data("coop_npd_major_greedy_2_250_" + n + "_p")[2])

    y_major = []
    y_err_major = []
    for instance in major_data:
        y_major.append(np.mean(instance))
        y_err_major.append(np.std(instance) / math.sqrt(len(instance)))


if __name__ == '__main__':
    for i in range(3, 11):
        print(calculate_coefficient(i))
