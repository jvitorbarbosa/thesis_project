from public_good_game import representative_society, society
from info_retrieval import *
from base import LearningParameters


def cooperation_rates_per_policy(agent_model, ruler, money, buckets, iterations=100, show=True):
    group_number = len(buckets)
    coop_rates = []
    for i in range(group_number):
        coop_rates.append([])
        for j in range(iterations):
            representative_society(agent_model, ruler, buckets[i], money, extract_info=get_coop_rates, info=coop_rates[i], show=False)
            if show:
                print("%3d/%d" % (j, iterations))
    return coop_rates


def cooperation_rates_per_param(agent_model, ruler, money, policy, iterations=100, show=True,
                                values=(0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1), param='alpha'):
    coop_rates = []
    modified_param = LearningParameters()
    for i in range(len(values)):
        coop_rates.append([])
        if param == 'alpha':
            modified_param.alpha = values[i]
        elif param == 'gamma':
            modified_param.gamma = values[i]
        else:
            print("Error: invalid parameter, possible parameters are 'alpha' and 'gamma'")
            break
        for j in range(iterations):
            representative_society(agent_model, ruler, policy, money, param=modified_param, extract_info=get_coop_rates, info=coop_rates[i], show=False)
            if show:
                print("%3d/%d" % (j, iterations))
    return coop_rates


def strategies_learned(agent_model, ruler, policy, money, iterations=100, show=True):
    strategies = []
    for i in range(iterations):
        citizens = []
        for c in range(ruler.citizens):
            citizens.append(agent_model(ruler, policy.copy(), money, LearningParameters()))
        citizens = society(citizens, show=False)
        sorted_int_vec = sorted([int(c.strategy(), base=2) for c in citizens])
        strategies.append([str(bin(n))[2:] for n in sorted_int_vec])
        if show:
            print("%3d/%d" % (i, iterations))
    return strategies


def strategies_exploration(agent_model, ruler, policy, money, iterations=100, show=True):
    strategies_changes = []
    for i in range(iterations//5):
        representative_society(agent_model, ruler, policy, money, extract_info=get_str_changes,
                               info=strategies_changes, learning_info=True, show=False, execution_rounds=0)
        if show:
            print("%3d/%d" % (i, iterations//5))
    return strategies_changes


def strategies_evolution(agent_model, ruler, policy, money, iterations=100, show=True):
    strategies_evo = []
    for i in range(iterations // 5):
        representative_society(agent_model, ruler, policy, money, extract_info=str_evo,
                               info=strategies_evo, learning_info=True, show=False, execution_rounds=0)
        if show:
            print("%3d/%d" % (i, iterations // 5))
    return strategies_evo


def policy_learned(learner, ruler, alpha, money, iterations=100, show=True):
    p_distribution = []
    order = []
    param = LearningParameters()
    for i in range(iterations):
        citizens = []
        for c in range(ruler.citizens):
            citizens.append(learner(ruler, ActorCriticLinear(alpha, param.alpha), money, param))
        citizens = society(citizens, show=False)
        for p in citizens:
            pol_dist = []
            if not order:
                order = [state for state in p.q_values.keys()]
            for state in order:
                if state in p.policy.coop_table.keys():
                    pol_dist.append(p.policy.coop_table[state])
                else:
                    pol_dist.append(0.5)
            p_distribution.append(pol_dist)
        if show:
            print("%3d/%d" % (i, iterations))
    average = np.mean(np.array(p_distribution), axis=0)
    variation = np.std(np.array(p_distribution), axis=0)
    print(order)
    print(average)
    print(variation)
    return average, variation


def pg_evolution(agent_model, ruler, policy, money, iterations=100, show=True):
    wealth_evo = []
    for i in range(iterations // 5):
        representative_society(agent_model, ruler, policy, money, extract_info=public_wealth_evo,
                               info=wealth_evo, learning_info=True, show=False, execution_rounds=0)
        if show:
            print("%3d/%d" % (i, iterations // 5))
    return wealth_evo


def pg_exec_evolution(agent_model, ruler, policy, money, iterations=100, show=True):
    wealth_evo = []
    for i in range(iterations):
        representative_society(agent_model, ruler, policy, money, extract_info=public_wealth_evo,
                               info=wealth_evo, learning_info=False, show=False)
        if show:
            print("%3d/%d" % (i, iterations))
    return wealth_evo


if __name__ == '__main__':
    from rulers import NPDRuler
    from social_learners import LevelLearner, SelflessLearner, MajorTDFour, AllOrNone
    from policies import ActorCriticLinear
    policy_learned(AllOrNone, NPDRuler(1, 5), 0.05, 20, iterations=1000)
