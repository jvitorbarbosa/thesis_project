from studio import strategy_hist
import pandas as pd


def main():
    data = pd.read_csv("oldraw/strategies_npd_major_grd--_2_1000_5_c1.txt").iloc[:, 1:].values

    strategy_hist("str_npd_major_grd-0001_2_1000_5.png", data, color=False)


main()
