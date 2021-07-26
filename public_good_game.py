import numpy as np
import pandas as pd
import random
from base import LearningParameters

TRAIN_ITERATIONS = 20000
EXEC_ITERATIONS = 1000
num_chart = 0


def society(players, extract_info=None, info=None, save=False, show=True, rounds=TRAIN_ITERATIONS):
    if not players:
        return []
    action_history = []
    str_history = []
    money_history = []
    for i in range(rounds):
        actions = {}
        strategies = []
        group_money = []
        for learner in players:
            actions[learner.id] = learner.act()
        for learner in players:
            learner.learn(actions)
            strategies.append(learner.strategy())
            group_money.append(learner.total_reward)
        action_history.append(list(actions.values()))
        str_history.append(strategies)
        money_history.append(group_money)

    if extract_info:
        extract_info(action_history, str_history, money_history, info)

    if show:
        pib = 0
        for i in range(len(players)):
            pib += players[i].total_reward
            print("Expected Reward = " + str(players[i].expected_reward()))
            print("Next Action = " + players[i].next_action.name)
        print("Society Wealth = " + str(pib))

    if save:
        act_file_name = str(num_chart) + "_" + str(len(players)) + "x" + str(players[0]) + "_act.txt"
        act_db = pd.DataFrame(data=np.array(action_history))
        act_db.to_csv(path_or_buf="raw/" + act_file_name)
        str_file_name = str(num_chart) + "_" + str(len(players)) + "x" + str(players[0]) + "_str.txt"
        str_db = pd.DataFrame(data=np.array(str_history))
        str_db.to_csv(path_or_buf="raw/" + str_file_name)
        money_file_name = str(num_chart) + "_" + str(len(players)) + "x" + str(players[0]) + "_wealth.txt"
        str_db = pd.DataFrame(data=np.array(money_history))
        str_db.to_csv(path_or_buf="raw/" + money_file_name)

    return players


def representative_society(agent_model, ruler, policy, money, param=LearningParameters(), extract_info=None, info=None, learning_info=False, save=False, show=True,
                           execution_rounds=EXEC_ITERATIONS, training_rounds=TRAIN_ITERATIONS):
    senators = []
    for i in range(ruler.citizens):
        people = []
        for groups in range(ruler.citizens):
            people.append(agent_model(ruler, policy.copy(), money, param))
        if learning_info:
            people = society(people, extract_info=extract_info, info=info, show=False, rounds=training_rounds)
        else:
            people = society(people, show=False, rounds=training_rounds)
        senators.append(random.choice(people))

    action_history = []
    str_history = []
    money_history = [[money]*ruler.citizens]
    for player in senators:
        player.reset()
    for i in range(execution_rounds):
        actions = {}
        group_money = []
        for player in senators:
            actions[player.id] = player.act(False)
        for player in senators:
            player.receive_consequences(actions)
            group_money.append(player.total_reward)
        action_history.append(list(actions.values()))
        money_history.append(group_money)

    for learner in senators:
        str_history.append(learner.strategy)

    if extract_info and not learning_info:
        extract_info(action_history, str_history, money_history, info)

    if show:
        pib = 0
        for i in range(len(senators)):
            pib += senators[i].total_reward
            print("Expected Reward = " + str(senators[i].expected_reward()))
            print("Next Action = " + senators[i].next_action.name)
        print("Society Wealth = " + str(pib))

    if save:
        act_file_name = str(num_chart) + "_" + str(len(senators)) + "x" + str(senators[0]) + "_sen.txt"
        act_db = pd.DataFrame(data=np.array(action_history))
        act_db.to_csv(path_or_buf="raw/" + act_file_name)
        money_file_name = str(num_chart) + "_" + str(len(senators)) + "x" + str(senators[0]) + "_wealth.txt"
        str_db = pd.DataFrame(data=np.array(money_history))
        str_db.to_csv(path_or_buf="raw/" + money_file_name)

    return senators


if __name__ == '__main__':
    from rulers import NPDRuler
    from social_learners import MajorTDFour
    from policies import EpsilonGreedy
    from info_retrieval import public_wealth_evo
    ruler = NPDRuler(1, 5)
    policy = EpsilonGreedy(0.001)
    players = []
    info = []
    for i in range(ruler.citizens):
        players.append(MajorTDFour(ruler, policy, 20))
    society(players, info=info, extract_info=public_wealth_evo, save=True)
    players = []
    for i in range(ruler.citizens):
        players.append(MajorTDFour(ruler, policy, 20))
    players = society(players, info=info, extract_info=public_wealth_evo, save=True)
    print(info)
    # representative_society(MajorTDFour, ruler, policy, 20, save=True)


