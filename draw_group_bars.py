from studio import paint_bars_in_groups
from base import compress_data
import math


def transpose_x_to_groups(data):
    new_data = []
    for i in range(len(data[0])):
        new_data.append([])
        for j in range(len(data)):
            new_data[i].append(data[j][i])
    return new_data


def main():
    labels = ["MemoryLess", "MajorTD4", "Selfless", "Level"]
    data1 = compress_data("coop_npd_nomem_lin_act_crt_2_250_5_p")
    data2 = compress_data("coop_npd_major_lin_act_crt_2_250_5_p")
    data3 = compress_data("coop_npd_selfless_lin_act_crt_2_250_5_p")
    data4 = compress_data("coop_npd_level_lin_act_crt_2_250_5_p")
    data = transpose_x_to_groups([data1, data2, data3, data4])
    # buckets = [math.pow(10, (-1) * i) for i in range(1, 7)]
    buckets = [0.05, 0.1, 0.3, 0.5, 0.7, 0.9, 1]
    paint_bars_in_groups("state_comparison4_greedy_2_1000_5.png", data, labels, y_label="Cooperation Rate",
                         x_label="Reinforcement Learning Player", candidates_label=buckets, color=False,
                         leg_title="\u03B1\u209A")


main()
