import pandas as pd
import numpy as np


def main():
    # policies = ["greedy", "grd-", "grd--", "dyn_lin_grd", "dyn_log_grd", "boltzmann", "lin_act_crt"]
    policies = ["lin_act_crt"]
    result = []
    for i in range(len(policies)):
        data = pd.read_csv("oldraw/str_changes_npd_level_" + policies[i] + "_2_1000_5_-05.txt").iloc[:, 1:].values
        result.append((policies[i], np.mean(data), np.std(data)))

    for pol, mean, dev in result:
        print("{0}: {1} +/- {2}".format(pol, mean, dev))


main()
