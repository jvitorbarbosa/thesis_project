import pandas as pd
from studio import paint_bars


def main():

    raw_data = []
    for i in range(1, 5):
        raw_data.append(pd.read_csv("raw/coop_npd_selfless_lin_act_crt_2_250_5_p" + str(i) + ".txt").iloc[:, 1:].values)
    data =[]
    for label in range(len(raw_data[0])):
        line = []
        for part in range(len(raw_data)):
            line += list(raw_data[part][label])
        data.append([line])
    labels = [0.05, 0.1, 0.3, 0.5, 0.7, 0.9, 1]

    paint_bars("lac_comparison_npd_selfless_2_1000_5.png", data, labels, y_label="Cooperation Rate",
               x_label="Policy Learning Rate Parameter", color=False)


main()
