from base import compress_data
from studio import paint_brackets


def main():
    raw_data = compress_data("coop_gamma_npd_major_grd-_2_250_5_p")
    labels = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    paint_brackets("gamma_npd_major_grd-_2_1000_5.png", raw_data, labels,
                   y_label="Cooperation Rate", x_label="Discounting Factor", color=False)


main()