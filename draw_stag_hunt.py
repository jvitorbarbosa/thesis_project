import pandas as pd
from studio import paint_bars


def main():
    raw_data = []
    for i in range(6):
        raw_data.append(pd.read_csv("raw/coop_stag_major_std_pol_2_1000_5_t" + str(i) + ".txt").iloc[:, 1:].values)

    labels = [0, 1, 2, 3, 4, 5]
    paint_bars("stag_hunt_threshold_major_std_pol_2_1000_5_p1.png", raw_data, labels,
               y_label="Cooperation Rate", x_label="Stag Hunt Threshold",
               data_index=0)


main()
