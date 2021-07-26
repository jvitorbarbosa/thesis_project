from studio import paint_bars
from base import compress_data


def main():
    labels = ["Epsilon\nGreedy", "Linear\nEpsilon", "Logarithmic\nEpsilon", "Boltzmann", "Actor-Critic"]
    eps_data = compress_data("coop_npd_major_greedy_2_250_5_p")[3]
    lin_data = compress_data("coop_npd_major_dyn_lin_grd_2_250_5_p")[2]
    log_data = compress_data("coop_npd_major_dyn_log_grd_2_250_5_p")[0]
    bolt_data = compress_data("coop_npd_major_boltzmann_2_250_5_p")[0]
    lac_data = compress_data("coop_npd_major_lin_act_crt_2_250_5_p")[6]

    data = [[eps_data], [lin_data], [log_data], [bolt_data], [lac_data]]

    paint_bars("policy_comparison_major_2_1000_5_n.png", data, labels,
               x_label="Policies", y_label="Cooperation Rate", color=False)


main()


