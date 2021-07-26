from base import *
import random
import math
import copy


class EpsilonGreedy(Policy):

    def __init__(self, epsilon):
        self.epsilon = epsilon

    def __str__(self):
        return "e-grd_" + str(self.epsilon)

    def choose(self, state, value_table, credit):
        if credit < 0:
            return Action.DEF
        new_action = Action.COOP
        if value_table[state][Action.DEF] > value_table[state][Action.COOP]:
            new_action = Action.DEF
        elif value_table[state][Action.COOP] == value_table[state][Action.DEF]:
            if random.random() < 0.5:
                new_action = Action.DEF
        if random.random() < self.epsilon:
            new_action = Action(not new_action)
        return new_action

    def copy(self):
        return EpsilonGreedy(self.epsilon)


class DynLinearEpsilonGreedy(EpsilonGreedy):

    def __init__(self, epsilon):
        super().__init__(epsilon)
        self.rounds = 1
        self.initial_epsilon = epsilon

    def choose(self, state, value_table, credit):
        new_action = super().choose(state, value_table, credit)
        self.rounds += 1
        self.epsilon = self.initial_epsilon / self.rounds
        return new_action

    def __str__(self):
        return "dyn_lin_grd_" + str(self.initial_epsilon)

    def copy(self):
        return DynLinearEpsilonGreedy(self.initial_epsilon)


class DynLogEpsilonGreedy(DynLinearEpsilonGreedy):

    def choose(self, state, value_table, credit):
        new_action = EpsilonGreedy.choose(self, state, value_table, credit)
        self.rounds += 1
        self.epsilon = self.initial_epsilon / math.log(self.rounds + 1)
        return new_action

    def __str__(self):
        return "dyn_log_grd_" + str(self.initial_epsilon)

    def copy(self):
        return DynLogEpsilonGreedy(self.initial_epsilon)


class Boltzmann(Policy):

    def __init__(self, beta):
        self.beta = beta

    def __str__(self):
        return "boltz_" + str(self.beta)

    def choose(self, state, value_table, credit):
        if credit < 0:
            return Action.DEF
        coop = math.exp(self.beta * value_table[state][Action.COOP])
        total = coop + math.exp(self.beta * value_table[state][Action.DEF])
        if random.random() < coop/total:
            return Action.COOP
        return Action.DEF

    def copy(self):
        return Boltzmann(self.beta)


class ActorCriticLinear(Policy):

    def __init__(self, alpha, sarsa_alpha):
        self.alpha = alpha
        self.sarsa_alpha = sarsa_alpha
        self.coop_table = {}
        self.last_action = Action.COOP
        self.last_table = {}
        self.last_state = None

    def __str__(self):
        return "act_crt" + str(self.alpha)

    def choose(self, state, value_table, credit):
        if state not in self.coop_table.keys():
            self.coop_table[state] = 0.5
        if self.last_state is not None:
            delta = value_table[self.last_state][self.last_action] - self.last_table[self.last_state][self.last_action]
            delta /= self.sarsa_alpha
            self.coop_table[self.last_state] += self.alpha * delta * \
                                                (self.last_action.value - self.coop_table[self.last_state])
        self.last_action = Action.DEF
        if credit > 0 and random.random() < self.coop_table[state]:
            self.last_action = Action.COOP
        self.last_state = state
        self.last_table = copy.deepcopy(value_table)
        return self.last_action

    def copy(self):
        return ActorCriticLinear(self.alpha, self.sarsa_alpha)


if __name__ == '__main__':
    from social_learners import MajorTDFour
    from public_good_game import society
    from rulers import NPDRuler
    ruler = NPDRuler(1, 5)
    policy = ActorCriticLinear(1)
    players = [MajorTDFour(ruler, policy.copy(), 20), MajorTDFour(ruler, policy.copy(), 20),
               MajorTDFour(ruler, policy.copy(), 20), MajorTDFour(ruler, policy.copy(), 20),
               MajorTDFour(ruler, policy.copy(), 20)]

    players = society(players, rounds=100)

    for p in players:
        print(p.policy.coop_table)
        print(p.total_reward)
