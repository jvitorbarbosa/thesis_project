from sympy import *
from public_good_game import *
import matplotlib.pyplot as plt
import matplotlib.axes as axes


def behavior_analysis(ruler, money, epsilon, iterations):
    record = [0.5]
    for i in range(iterations):
        representative_society(ruler, money, epsilon, show=False, save=record)
        print(str(i+1) + "/" + str(iterations))
    record = record[1:]
    frequencies = []
    cooperators = 0
    for i in range(len(record)):
        if record[i] > 0.8:
            cooperators += 1
        if (i+1) % 5 == 0:
            frequencies.append(cooperators)
            cooperators = 0

    return frequencies


def strategy_analysis(ruler, money, epsilon, iterations):
    bag = []
    for i in range(iterations):
        players = representative_society(ruler, money, epsilon, show=False)
        for p in players:
            bag.append(p.strategy().name)
        print(str(i + 1) + "/" + str(iterations))
    return bag


def frequency_epsilon_graphic(ruler, money, name, iterations=100):
    fre1 = behavior_analysis(ruler, money, 0, iterations)
    fre2 = behavior_analysis(ruler, money, 0.01, iterations)
    fre3 = behavior_analysis(ruler, money, 0.001, iterations)
    fre4 = behavior_analysis(ruler, money, 0.0001, iterations)

    fig, ax = plt.subplots(2, 2)
    hfont = {"fontname": "Arial"}

    ax[0, 0].hist(fre1, range=(-0.5, 5.5), bins=6)
    ax[0, 1].hist(fre2, range=(-0.5, 5.5), bins=6)
    ax[1, 0].hist(fre3, range=(-0.5, 5.5), bins=6)
    ax[1, 1].hist(fre4, range=(-0.5, 5.5), bins=6)

    ax[0, 0].set_ylabel("Frequency", **hfont)
    ax[1, 0].set_ylabel("Frequency", **hfont)
    ax[1, 1].set_ylabel("Frequency", **hfont)
    ax[0, 1].set_ylabel("Frequency", **hfont)

    ax[0, 0].set_xlabel("Number of Cooperators", **hfont)
    ax[1, 0].set_xlabel("Number of Cooperators", **hfont)
    ax[1, 1].set_xlabel("Number of Cooperators", **hfont)
    ax[0, 1].set_xlabel("Number of Cooperators", **hfont)

    ax[0, 0].set_title("\u03B5 = 0", **hfont)
    ax[0, 1].set_title("\u03B5 = 0.01", **hfont)
    ax[1, 0].set_title("\u03B5 = 0.001", **hfont)
    ax[1, 1].set_title("\u03B5 = 0.0001", **hfont)

    axes.Axes.set_xticks(ax[0, 0], [0, 1, 2, 3, 4, 5])
    axes.Axes.set_xticks(ax[0, 1], [0, 1, 2, 3, 4, 5])
    axes.Axes.set_xticks(ax[1, 0], [0, 1, 2, 3, 4, 5])
    axes.Axes.set_xticks(ax[1, 1], [0, 1, 2, 3, 4, 5])

    fig.tight_layout()
    plt.savefig(name, bbox_inches='tight')
    plt.close()


def strategy_epsilon_graphic(ruler, money, name, iterations=100):
    bag1 = strategy_analysis(ruler, money, 0, iterations)
    bag2 = strategy_analysis(ruler, money, 0.01, iterations)
    bag3 = strategy_analysis(ruler, money, 0.001, iterations)
    bag4 = strategy_analysis(ruler, money, 0.0001, iterations)

    fig, ax = plt.subplots(2, 2)
    hfont = {"fontname": "Arial"}

    limit1 = len(set(bag1))
    limit2 = len(set(bag2))
    limit3 = len(set(bag3))
    limit4 = len(set(bag4))

    plt.setp(ax[0, 0].get_xticklabels(), rotation=90, horizontalalignment='center')
    plt.setp(ax[0, 1].get_xticklabels(), rotation=90, horizontalalignment='center')
    plt.setp(ax[1, 0].get_xticklabels(), rotation=90, horizontalalignment='center')
    plt.setp(ax[1, 1].get_xticklabels(), rotation=90, horizontalalignment='center')

    ax[0, 0].hist(bag1, range=(-0.5, limit1 - 0.5), bins=limit1)
    ax[0, 1].hist(bag2, range=(-0.5, limit2 - 0.5), bins=limit2)
    ax[1, 0].hist(bag3, range=(-0.5, limit3 - 0.5), bins=limit3)
    ax[1, 1].hist(bag4, range=(-0.5, limit4 - 0.5), bins=limit4)

    ax[0, 0].set_ylabel("Frequency", **hfont)
    ax[1, 0].set_ylabel("Frequency", **hfont)
    ax[1, 1].set_ylabel("Frequency", **hfont)
    ax[0, 1].set_ylabel("Frequency", **hfont)

    ax[0, 0].set_xlabel("Learned Strategies", **hfont)
    ax[1, 0].set_xlabel("Learned Strategies", **hfont)
    ax[1, 1].set_xlabel("Learned Strategies", **hfont)
    ax[0, 1].set_xlabel("Learned Strategies", **hfont)

    ax[0, 0].set_title("\u03B5 = 0", **hfont)
    ax[0, 1].set_title("\u03B5 = 0.01", **hfont)
    ax[1, 0].set_title("\u03B5 = 0.001", **hfont)
    ax[1, 1].set_title("\u03B5 = 0.0001", **hfont)

    fig.tight_layout()
    plt.savefig(name, bbox_inches='tight')
    plt.close()


def dyn_epsilon_analysis(name="test.png", iterations=100):
    ruler = NPDRuler(1, 5)
    f = behavior_analysis(ruler, 100, 0.01, iterations)
    b = strategy_analysis(ruler, 100, 0.01, iterations)

    fig, ax = plt.subplots(2, 1)
    hfont = {"fontname": "Arial"}

    limit = len(set(b))

    plt.setp(ax[1].get_xticklabels(), rotation=90, horizontalalignment='center')

    ax[0].hist(f, range=(-0.5, 5.5), bins=6)
    ax[1].hist(b, range=(-0.5, limit - 0.5), bins=limit)

    ax[0].set_ylabel("Frequency", **hfont)
    ax[1].set_ylabel("Frequency", **hfont)

    ax[0].set_xlabel("Number of Cooperators", **hfont)
    ax[1].set_xlabel("Learned Strategies", **hfont)

    fig.tight_layout()
    plt.savefig(name, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    # print("Start")
    # ruler = RiskyRuler(2, 0.1, 1, 5, threshold=2)
    # frequency_epsilon_graphic(ruler, 100, "CRD_2_freq_epsilon.png")
    # strategy_epsilon_graphic(ruler, 100, "CRD_2_str_epsilon.png")
    # print("Part1")
    # ruler1 = RiskyRuler(2, 0.1, 1, 5, threshold=3)
    # frequency_epsilon_graphic(ruler1, 100, "CRD_3_freq_epsilon.png")
    # strategy_epsilon_graphic(ruler1, 100, "CRD_3_str_epsilon.png")
    # print("Part2")
    # ruler2 = RiskyRuler(2, 0.1, 1, 5, threshold=4)
    # frequency_epsilon_graphic(ruler2, 100, "CRD_4_freq_epsilon")
    # strategy_epsilon_graphic(ruler2, 100, "CRD_4_str_epsilon.png")
    # print("Part3")

    # dyn_epsilon_analysis(name="dyn_eps_study_01.png")

    frequency_epsilon_graphic(NPDRuler(1, 5), 100, "NPD_LL_freq_epsilon.png")


