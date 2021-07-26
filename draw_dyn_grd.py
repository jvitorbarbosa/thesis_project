from studio import paint_bars
from base import compress_data
import math
import pandas as pd

def main():
    data = compress_data("coop_npd_allornone_lin_act_crt_2_250_5_p", is_group_bars=False)
    # raw_data = pd.read_csv("raw/coop_npd_allornone_lin_act_crt_2_100_5_t1.txt").iloc[:, 1:].values
    # data = [[item] for item in raw_data]
    # labels = [str(math.pow(10, (-1) * i)) for i in range(1, 7)]
    # labels.reverse()
    labels = [0.05, 0.1, 0.3, 0.5, 0.7, 0.9, 1]
    paint_bars("grd_allornone_2_1000_5.png", data, labels,
               y_label="Cooperation Rate", x_label="Policy learning rate",
               data_index=0, color=True)


main()
