from base import compress_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


def main():

    labels = [str(i) for i in range(3, 11)]
    data_index = 2
    level_data = []
    selfless_data = []
    major_data = []
    leg_label = ["Major", "Selfless", "Level"]

    # LOAD MAJOR
    for n in labels:
        major_data.append(compress_data("coop_npd_major_greedy_2_250_" + n + "_p")[2])

    # LOAD LEVEL
    for n in labels:
        if n == "5":
            level_data.append(compress_data("coop_npd_level_greedy_2_250_5_p")[2])
        elif n in ["9", "10"]:
            level_data.append(compress_data("coop_npd_level_std_pol_2_250_" + n + "_p")[0])
        else:
            level_data.append(pd.read_csv("raw/coop_npd_level_std_pol_2_1000_" + n + "_p1.txt").iloc[0, 1:].values)


    # LOAD SELFLESS
    for n in labels:
        if n == "5":
            selfless_data.append(compress_data("coop_npd_selfless_greedy_2_250_5_p")[data_index])
        else:
            selfless_data.append(pd.read_csv("raw/coop_npd_selfless_std_pol_2_1000_" + n + "_p1.txt").iloc[0, 1:].values)

    x_label = "Population Size"""
    y_label = "Cooperation Rate"
    leg = []
    x_plot = [int(i) for i in labels]
    y_level = []
    y_err_level = []
    y_selfless = []
    y_err_selfless = []
    y_major = []
    y_err_major = []
    for instance in level_data:
        y_level.append(np.mean(instance))
        y_err_level.append(np.std(instance) / math.sqrt(len(instance)))
    for instance in selfless_data:
        y_selfless.append(np.mean(instance))
        y_err_selfless.append(np.std(instance) / math.sqrt(len(instance)))
    for instance in major_data:
        y_major.append(np.mean(instance))
        y_err_major.append(np.std(instance) / math.sqrt(len(instance)))

    print(x_plot)
    print(y_major)
    print(y_selfless)
    print(y_level)

    plt.style.use("grayscale")
    plt.rcParams.update({'font.size': 14, "lines.markersize": 4, "lines.linewidth": 0.5, "legend.fontsize": "small"})
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    leg.append(plt.errorbar(x_plot, y_major, yerr=y_err_major, fmt='s-', solid_capstyle='projecting', capsize=5)[0])
    leg.append(plt.errorbar(x_plot, y_selfless, yerr=y_err_selfless, fmt='^-', solid_capstyle='projecting', capsize=5)[0])
    leg.append(plt.errorbar(x_plot, y_level, yerr=y_err_level, fmt='o-', solid_capstyle='projecting', capsize=5)[0])
    plt.legend(leg, leg_label, title="Player", loc=1)

    plt.savefig("pop_comparison_std_pol_2_1000.png", bbox_inches='tight')
    plt.close()


main()
