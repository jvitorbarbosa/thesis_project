import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd


def paint_bars_in_groups(name, data, buckets, y_label="", x_label="", candidates_label=None, leg_loc=2, color=True, leg_title=""):
    group_number = len(buckets)
    y = []
    y_err = []
    if not candidates_label:
        candidates_label = []
    for instance in data:
        y.append([])
        y_err.append([])
        for i in range(group_number):
            y[-1].append(np.mean(np.array(instance[i])))
            y_err[-1].append(np.std(np.array(instance[i]))/math.sqrt(len(instance[i])))
    print(y)
    print(buckets)
    plt.figure(1)
    width = 0.6 / len(data)
    leg = []
    gray_int = 0.0
    plt.rcParams.update({'font.size': 14})
    for i in range(len(data)):
        color_str = None
        if not color:
            gray_int += 0.12
            color_str = str(gray_int)
        if len(candidates_label) < len(data):
            candidates_label.append("G{0}".format(i))
        leg.append(plt.bar(np.arange(group_number) + i * width, y[i], width,
                           color=color_str, bottom=0, yerr=y_err[i])[0])
    plt.legend(leg, candidates_label, title=leg_title, loc=leg_loc)
    labels = [str(b) for b in buckets]
    plt.xticks(np.arange(group_number) + (width / 2) * (len(data) - 1), labels)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.savefig(name, bbox_inches='tight')
    plt.close()


def paint_bars(name, data, buckets, y_label="", x_label="", data_index=0, color=True):
    y = []
    y_err = []
    for instance in data:
        y.append(np.mean(instance[data_index]))
        y_err.append(np.std(instance[data_index]) / math.sqrt(len(instance[data_index])))
    print(y)
    plt.figure(figsize=(8, 4))
    if not color:
        plt.style.use("grayscale")
    plt.rcParams.update({'font.size': 14})
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.bar(np.arange(len(buckets)), y, yerr=y_err, width=0.5)
    plt.xticks(np.arange(len(buckets)), buckets)
    plt.savefig(name, bbox_inches='tight')
    plt.close()


def paint_brackets(name, data, buckets, y_label="", x_label="", color=True):
    y = []
    y_err = []
    for instance in data:
        y.append(np.mean(instance))
        y_err.append(np.std(instance) / math.sqrt(len(instance)))
    print(y)
    print(buckets)
    plt.figure(figsize=(8, 4))
    if not color:
        plt.style.use("grayscale")
    plt.rcParams.update({'font.size': 14})
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.errorbar(np.arange(len(buckets)), y, yerr=y_err, fmt='.-', solid_capstyle='projecting', capsize=5)
    plt.xticks(np.arange(len(buckets)), buckets)
    plt.savefig(name, bbox_inches='tight')
    plt.close()


def strategy_hist(name, data, y_label="Strategy Frequency", x_label="Learned Strategies", color=True):
    bag = []
    for line in data:
        for item in ["S" + str(int(str(s), base=2)) for s in line]:
            std_item = item
            if len(item) < 3:
                std_item = item[0] + "0" + item[1]
            bag.append(std_item)
    print(bag)

    fig = plt.figure(1)
    hfont = {"fontname": "Arial"}
    if not color:
        plt.style.use("grayscale")

    limit = len(set(bag))

    plt.xticks(rotation='vertical')

    plt.hist(bag, range=(-0.5, limit - 0.5), bins=limit)

    plt.ylabel(y_label, **hfont)

    plt.xlabel(x_label, **hfont)

    fig.tight_layout()
    plt.savefig(name, bbox_inches='tight')
    plt.close()


def consolidate_pg_growth_table(name):
    instances = ["major_grd-", "major_dyn_lin_grd", "major_dyn_log_grd", "major_boltzmann",
                 "major_lin_act_crt", "selfless_lin_act_crt-", "level_lin_act_crt-"]
    final_table = []
    for i in range(len(instances)):
        row = [instances[i]]
        data = pd.read_csv("raw/pg_evo_npd_" + instances[i] + "_2_1000_5_l1.txt").iloc[:, 1:].values
        for line in data:
            row.append(np.mean(line))
        final_table.append(row)
    db = pd.DataFrame(data=np.array(final_table))
    db.to_csv(path_or_buf="raw/" + name)


def consolidate_pg_final(name):
    instances = ["major_grd-", "major_dyn_lin_grd", "major_dyn_log_grd", "major_boltzmann",
                 "major_lin_act_crt", "selfless_lin_act_crt-"]
    labels = ["major\ngrd", "major\nlin_grd", "major\nlog_grd", "major\nboltz",
                 "major\nlac", "selfless\nlac"]
    y = []
    y_err = []
    for i in range(len(instances)):
        data = pd.read_csv("raw/pg_evo_npd_" + instances[i] + "_2_1000_5_p1.txt").iloc[:, 1:].values
        y.append(np.mean(data[-1]))
        y_err.append(np.std(data[-1])/len(data[-1]))
    plt.figure(figsize=(6.4, 3.2))
    plt.xlabel("Agent Variations")
    plt.ylabel("Total Wealth")
    plt.rcParams.update({'font.size': 9})
    plt.errorbar(np.arange(len(instances)), y, yerr=y_err, fmt='-o', markersize=2, capsize=5)
    plt.xticks(np.arange(len(instances)), labels)
    plt.savefig(name, bbox_inches='tight')
    plt.close()



if __name__ == '__main__':
    consolidate_pg_growth_table("wealth_history_learning.csv")
    # consolidate_pg_final("pg_final_learning.png")


