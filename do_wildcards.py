import pandas as pd
import sys
import numpy as np


def single_hamming(s1, s2):
    dist = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            dist += 1
    return dist


# There are two command line parameters: p1 p2
# p1: path to the input file (valid path).
# p2: is a float of how predominant the wildcard must be.
def main():
    threshold = float(sys.argv[2])
    data = pd.read_csv(sys.argv[1])
    data = data.iloc[:, 1:]
    stream = []
    for i in range(len(data)):
        data.iloc[i, :] = ["{0:{fill}4b}".format(j, fill='0') for j in data.iloc[i, :]]
    for i in range(len(data.iloc[0, :])):
        stream += list(data.iloc[:, i].values)
    N = len(stream)
    unique = np.unique(data)
    wildcards = []
    for item in unique:
        for i in range(len(item)):
            wildcard = item[:i] + 'x' + item[i+1:]
            wildcards.append(wildcard)
    candidates = list(set(wildcards))
    print(candidates)
    popularity = {}
    for candidate in candidates:
        for item in stream:
            if single_hamming(candidate, item) == 1:
                if candidate in popularity.keys():
                    popularity[candidate] += 1
                else:
                    popularity[candidate] = 0

    for key, value in popularity.items():
        if value >= threshold * N:
            print(key)


main()
