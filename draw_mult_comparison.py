from studio import paint_brackets
from base import compress_data


def main():
    labels = ["2", "3", "5", "7", "10"]
    data_index = 2
    data = []
    for label in labels:
        data.append(compress_data("coop_npd_major_greedy_" + label + "_250_5_p")[data_index])

    paint_brackets("mult_comparison_major_greedy_001_1000.png", data, labels,
               "Cooperation Rate", "Public Good Multiplier", color=False)

    # buckets = [math.pow(10, (-1) * i) for i in range(1, 7)]
    # paint_bars_in_groups("mult_epsilon_comparison_major_greedy_1000.png", data, buckets, y_label="Cooperation Rate",
    #                      x_label="Epsilon Values", candidates_label=labels, leg_loc=4)


main()
