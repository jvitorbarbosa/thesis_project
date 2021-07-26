from studio import paint_bars
import math
import numpy as np
import matplotlib.pyplot as plt
from base import compress_data


# Old values equal to epsilon [10^-1, 10^-2, 10^-3, 10^-4, 10^-5, 10^-6]
# New values are 7 equal distanced points between 0.1 and 1.
def main():
    data = compress_data("major_boltzmann", is_group_bars=False)
    labels = [str(math.pow(10, i-2)) for i in range(4)]
    # y = []
    # y_err = []
    # for instance in data:
    #     y.append(np.mean(np.array(instance)))
    #     y_err.append(np.std(np.array(instance)) / math.sqrt(len(instance)))
    # plt.figure(1)
    # plt.bar(np.arange(len(data)), y, yerr=y_err)
    # plt.xlabel("Beta Parameter Value")
    # plt.ylabel("Cooperation Rate")
    # plt.xticks(np.arange(len(data)), labels)
    # plt.savefig("boltz_comparison_major_2_1000_5.png", bbox_inches='tight')
    # plt.close()

    paint_bars("boltz_comparison_major_2_1000_5.png", data, labels, y_label="Cooperation Rate",
               x_label="Beta Parameter Value", color=False)


main()
