import numpy as np
import random


def euclidean(v1, v2):
    return np.linalg.norm(v1 - v2)


class KMedoids:

    def __init__(self, distance_function=euclidean, n_clusters=2):
        self.data = []
        self.distance = distance_function
        self.k = n_clusters
        self.current_medoids = []
        self.error = float('Inf')
        self.inertia_ = self.error
        self.labels_ = []

    def get_medoids(self):
        medoids = []
        for index in self.current_medoids:
            medoids.append(self.data[index])
        return np.array(medoids)

    def fit(self, data):
        self.data = data
        self.current_medoids = [random.randrange(0, len(data)) for i in range(self.k)]
        self.error = float('Inf')
        current_error, self.labels_ = self.calculate_error(self.current_medoids)
        while self.error > current_error:
            self.error = current_error
            changed = False
            for instance in range(len(self.data)):
                if instance not in self.current_medoids:
                    for i in range(self.k):
                        candidates = self.current_medoids[:i] + [instance] + self.current_medoids[i+1:]
                        current_error, candidate_labels = self.calculate_error(candidates)
                        if current_error < self.error:
                            self.current_medoids = candidates
                            self.labels_ = candidate_labels
                            changed = True
                            break
                    if changed:
                        break
        self.inertia_ = self.error

    def calculate_error(self, candidates):
        accumulated_error = 0
        labels = [-1] * len(self.data)
        for index in range(len(self.data)):
            if index not in candidates:
                smaller_diff = float('Inf')
                for m in candidates:
                    pair_distance = self.distance(self.data[index], self.data[m])
                    if pair_distance < smaller_diff:
                        smaller_diff = pair_distance
                        labels[index] = m
                accumulated_error += smaller_diff
        return accumulated_error, labels

    def transform(self, test):
        accumulated_error = 0
        for item in test:
            smaller_diff = float('Inf')
            for medoid in self.current_medoids:
                pair_distance = self.distance(item, self.data[medoid])
                if pair_distance < smaller_diff:
                    smaller_diff = pair_distance
            accumulated_error += smaller_diff
        return accumulated_error


def hamming(s1, s2):
    if len(s1) != len(s2):
        return np.nan
    dist = 0
    ss1 = ""
    ss2 = ""
    for i in range(len(s1)):
        ss1 += s1[i]
        ss2 += s2[i]
    for i in range(len(ss1)):
        if ss1[i] != ss2[i]:
            dist += 1
    return dist


if __name__ == '__main__':
    import pandas as pd
    data = pd.read_csv("raw/strategies_i-100.txt")
    data = data.iloc[:, 1:]

    for i in range(len(data)):
        data.iloc[i, :] = ["{0:{fill}4b}".format(j, fill='0') for j in data.iloc[i, :]]
    print(data.iloc[1])
    print(data.iloc[2])
    print(hamming(data.iloc[1], data.iloc[2]))
    # print(data)
    # # data = data.iloc[:, 1:]
    # # print(data)
    # km = KMedoids(n_clusters=5, distance_function=hamming)
    # # print(km.get_medoids())
    # km.fit(data.values)
    # print(km.get_medoids())
    # test = data.iloc[10:20, :].values
    # print(test)
    # print(km.transform(test))












