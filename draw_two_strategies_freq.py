import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def main():
    name = "two_str_comparison_e001_lac1.png"

    y_label = "Strategy Frequency"
    x_label = "Learned Strategies"
    str_names = ["S{0:02d}".format(i) for i in range(16)]

    count1 = [0] * 16
    data1 = pd.read_csv("oldraw/strategies_npd_major_lin_act_crt_2_1000_5_ff.txt").iloc[:, 1:].values
    for line in data1:
        for item in [int(str(s), base=2) for s in line]:
            count1[item] += 1

    count2 = [0] * 16
    data2 = pd.read_csv("oldraw/strategies_npd_major_grd-_2_1000_5_c1.txt").iloc[:, 1:].values
    for line in data2:
        for item in [int(str(s), base=2) for s in line]:
            count2[item] += 1

    fig = plt.figure(1)

    plt.style.use("grayscale")
    plt.rcParams.update({'font.size': 14})

    plt.xticks(np.arange(16), str_names, rotation='vertical')

    out1 = plt.plot(np.arange(16), count1, '-o')
    out2 = plt.plot(np.arange(16), count2, '-o')

    plt.legend(["Actor-Critic (\u03B1\u209A=1)", "\u03B5-greedy(\u03B5=0.001)"], title="Learning Policies", loc=0)

    plt.ylabel(y_label)
    plt.xlabel(x_label)

    fig.tight_layout()
    plt.savefig(name, bbox_inches='tight')
    plt.close()


main()