import numpy as np
from base import Action


def get_coop_rates(act_history, str_history, money_history, info):
    last_players_action = np.transpose(np.array(act_history[-100:]))
    for p in last_players_action:
        info.append((np.count_nonzero(p == Action.COOP))/100)


def get_str_changes(act_history, str_history, money_history, info):
    changes = []
    for i in range(len(str_history[0])):
        changes.append(0)
    last_values = str_history[0]
    for line in str_history:
        for i in range(len(line)):
            if line[i] != last_values[i]:
                changes[i] += 1
        last_values = line
    info.append(changes)


def str_evo(act_history, str_history, money_history, info):
    if not info:
        for i in range(len(str_history)):
            info.append([])
    for index in range(len(str_history)):
        info[index] += str_history[index]


def wealth_produced(act_history, str_history, money_history, info):
    info.append(np.sum(money_history[-1]))


def public_wealth_evo(act_history, str_history, money_history, info):
    if not info:
        for i in range(len(money_history)):
            info.append([])
    for index in range(len(money_history)):
        info[index].append(np.sum(money_history[index]))


if __name__ == '__main__':
    str_evo([], [[1], [2], [3]], [[0], [0], [0]])
