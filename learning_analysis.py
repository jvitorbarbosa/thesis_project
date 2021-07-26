from public_good_game import NPDRuler, TRAIN_ITERATIONS
import matplotlib.pyplot as plt
import math
import pandas as pd
import numpy as np

FIGNUM = 0


def show_str_evolution(data):
    y = []
    x = []
    x_label = []
    for st, r in data:
        x.append(r if r == 0 else math.log(r))
        x_label.append("")
        if not y:
            for item in st:
                y.append([int(item.name[1:])])
        else:
            for i in range(len(st)):
                y[i].append(int(st[i].name[1:]))
    global FIGNUM
    ax = plt.subplot(111)
    name = "str_evo_dyn_" + str(FIGNUM) + ".png"
    plt.grid(True)
    ax.set_xticks(x)
    ax.set_xticklabels(x_label)
    # plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='center')
    for i in range(len(y)):
        plt.plot(x, y[i])
    plt.savefig(name, bbox_inches='tight')
    FIGNUM += 1
    # plt.show()
    plt.close()


def show_coop_evolution(data):
    y_temp = []
    x = []
    for st, r in data:
        x.append(r if r == 0 else math.log(r))
        if not y_temp:
            for item in st:
                y_temp.append([item.value])
        else:
            for i in range(len(st)):
                y_temp[i].append(st[i].value)

    y = []
    # print(y_temp[0][:100])
    for i in range(len(data) - 100):
        if not y:
            for j in range(len(y_temp)):
                y.append([y_temp[j][i:i+100].count(1)])
        else:
            for j in range(len(y_temp)):
                y[j].append(y_temp[j][i:i+100].count(1))

    # print(y[0][:100])
    plt.figure()
    for i in range(len(y)):
        plt.plot(x[100:], y[i])
    plt.savefig("evolution.png", bbox_inches='tight')
    plt.show()
    plt.close()


def compare_str_coop(id, rounds=TRAIN_ITERATIONS):
    str_database = pd.read_csv(str(id) + "_evolution_through_" + str(rounds) + ".txt")
    coop_database = pd.read_csv(str(id) + "_cooperation_through_" + str(rounds) + ".txt")

    name = str(id) + "_str_coop_0001" + ".png"
    fig, ax = plt.subplots(2, 1)
    x = str_database.iloc[:, -1].values
    x = np.log(x)
    ax[0].grid(True)
    ax[0].set_xticks(x)
    ax[0].set_xticklabels([""] * str_database.shape[0])
    for i in range(str_database.shape[1]-1):
        ax[0].plot(x, str_database.iloc[:, i].values)

    x_coop = np.log(coop_database.iloc[:, -1].values)
    cooperation = []
    for i in range(coop_database.shape[1]):
        cooperation.append([])
    for i in range(coop_database.shape[0] - 100):
        print(i)
        for j in range(coop_database.shape[1]-1):
            cooperation[j].append(np.sum(coop_database.iloc[i:i+100, j].values)/100)

    for i in range(coop_database.shape[1]-1):
        ax[1].plot(x_coop[100:], cooperation[i])
    plt.savefig(name, bbox_inches='tight')
    # plt.show()
    plt.close()


if __name__ == '__main__':
    # for i in range(10):
    #     print(i)
    #     show_str_evolution(long_run(MajorityRuler(1, 5), 20, 0.1, []))
    for i in range(10, 15):
        print("GAME = " + str(i))
        full_long_run(i, NPDRuler(1, 5), 20, 0.0001, [])
        compare_str_coop(i)
    # show_coop_evolution(action_long_run(MajorityRuler(1, 5), 20, 0, []))

