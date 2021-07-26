import matplotlib.pyplot as plt

MAX_RUNS = 20000
num_chart = 1


def duel(learner, opp, show=True, save=False, rounds=MAX_RUNS):
    history = 100 * [Action.COOP]
    opp_history = 100 * [Action.COOP]
    data = []
    opp_data = []
    for i in range(rounds):
        c = 0
        opp_c = 0
        for j in range(i, i + 100):
            if history[j] == Action.COOP:
                c += 1
            if opp_history[j] == Action.COOP:
                opp_c += 1
        data.append(c / 100)
        opp_data.append(opp_c / 100)
        actions = {learner.id: learner.act(), opp.id: opp.act()}
        learner.judge.analyse_case(actions)
        opp.judge.analyse_case(actions)
        learner.learn(actions)
        opp.learn(actions)
        history.append(actions[learner.id])
        opp_history.append(actions[opp.id])

    if show or save:
        print("Player Expected Reward = " + str(learner.expected_reward()))
        print("Opponent Expected Reward = " + str(opp.expected_reward()))
        global num_chart
        plt.figure(num_chart)
        ax = [plt.plot(data)[0], plt.plot(opp_data)[0]]
        name = str(learner) + "_vs_" + str(opp) + ".png"
        plt.legend(ax, [str(learner), str(opp)])
        if save:
            plt.savefig(name, bbox_inches='tight')
        if show:
            plt.show()
        plt.close(num_chart)
        num_chart += 1


def td4_war(learner, nrounds, nbattles):
    total = [MemoryState('{:04b}'.format(x)) for x in range(16)]
    opponents = [MemoryState('{:04b}'.format(x)) for x in range(16)]
    labels = [t.name for t in total]
    data = []
    for i in range(len(total)):
        data.append([0]*len(opponents))
    for opp in opponents:
        results = [0] * len(total)
        o = opponents.index(opp)
        for battle in range(nbattles):
            print("%4.d/%4.d" % (o*nbattles + battle + 1, nbattles*len(opponents)))  # Show progress during execution
            duel(learner, MemoryOne(learner.judge, opp, 0.01), rounds=nrounds, show=False)
            results[total.index(learner.strategy())] += 1

        for i in range(len(total)):
            data[i][o] = float(results[i])/nbattles

    plt.figure(figsize=(8, 4), dpi=120)
    plt.table(cellText=data, rowLabels=labels, colLabels=labels, cellLoc='center', loc='upper left')
    plt.axis('off')
    plt.savefig("td4_war.png", bbox_inches='tight')


if __name__ == '__main__':
    from td_learning import TDOne, TDTwo, TDFour
    from rulers import PayoffMatrix
    from opponent import *
    from policies import EpsilonGreedy
    policy = EpsilonGreedy(0.01)
    std_judge = PayoffMatrix(3, 0, 5, 1)
    duel(TitForTat(std_judge), AlwaysCoop(std_judge))
    duel(TDOne(std_judge, policy), AlwaysCoop(std_judge))
    duel(TDOne(std_judge, policy), AlwaysDef(std_judge))
    duel(TDOne(std_judge, policy), Alternate(std_judge))
    duel(TDOne(std_judge, policy), TitForTat(std_judge))
    duel(TDTwo(std_judge, policy), TitForTat(std_judge))
    duel(TDTwo(std_judge, policy), Reactive(std_judge, 1, 0))
    duel(TDTwo(std_judge, policy), Reactive(std_judge, 1, 1))
    duel(TDTwo(std_judge, policy), Reactive(std_judge, 0.8, 0.2))
    duel(TDTwo(std_judge, policy), Reactive(std_judge, 0.6, 0.5))
    duel(TDFour(std_judge, policy), TitForTat(std_judge))
    duel(TDFour(std_judge, policy), Reactive(std_judge, 1, 0))
    duel(TDFour(std_judge, policy), Reactive(std_judge, 1, 1))
    duel(TDFour(std_judge, policy), Reactive(std_judge, 0.8, 0.2))
    duel(TDFour(std_judge, policy), Reactive(std_judge, 0.6, 0.5))
    duel(TDTwo(std_judge, policy), TitForTwoTat(std_judge))
    duel(TDFour(std_judge, policy), TitForTwoTat(std_judge))
    duel(TDTwo(PayoffMatrix(4, 0, 5, 1), policy), WinStayLooseShift(std_judge))   # change in R to catch special situation
    duel(TDFour(PayoffMatrix(4, 0, 5, 1), policy), WinStayLooseShift(std_judge))  # where TDTwo fails and TDFour thrives
    duel(TDTwo(std_judge, policy), TDTwo(std_judge, policy))
    duel(TDFour(std_judge, policy), TDFour(std_judge, policy))
    # td4_war(TDFour(std_judge, policy), 10000, 100)
