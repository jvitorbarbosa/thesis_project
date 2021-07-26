from base import *
import random


class NPDRuler(Judge):

    def __init__(self, payment, citizens, f=2):
        super().__init__(payment, citizens)
        self.f = f
        self.recent_cooperators = 0

    def analyse_case(self, accusing):
        self.recent_cooperators = list(accusing.values()).count(Action.COOP)

    def sentence(self, respondent):
        reward = self.f * self.recent_cooperators * self.payment / self.citizens
        if respondent == Action.COOP:
            reward -= self.payment
        return reward


class ThresholdRuler(NPDRuler):

    def __init__(self, payment, citizens, f=2, threshold=0):
        super().__init__(payment, citizens, f)
        self.threshold = threshold
        if threshold == -1:
            self.threshold = citizens/2

    def sentence(self, respondent):
        reward = 0
        if self.recent_cooperators >= self.threshold:
            reward = self.f * self.recent_cooperators * self.payment / self.citizens
        if respondent == Action.COOP:
            reward -= self.payment
        return reward


class RiskyRuler(ThresholdRuler):

    def __init__(self, benefit, risk, payment, citizens, f=2, threshold=0):
        super().__init__(payment, citizens, f, threshold)
        self.benefit = benefit
        self.risk = risk

    def sentence(self, respondent):
        reward = self.benefit
        if self.recent_cooperators < self.threshold and random.random() < self.risk:
            reward = 0
        if respondent == Action.COOP:
            reward -= self.payment
        return reward


class PayoffMatrix(Judge):

    def __init__(self, r, s, t, p, payment=0, citizens=2):
        super().__init__(payment, citizens)
        self.dict = {'r': r, 's': s, 't': t, 'p': p}
        self.matrix = [[p, t], [s, r]]
        self.cooperators = 0

    def is_prisoners_dilemma(self):
        return (self.dict['t'] > self.dict['r'] > self.dict['p'] > self.dict['s'] and
                self.dict['r'] > (self.dict['t'] + self.dict['s']) / 2)

    def sentence(self, respondent):
        other_coop = self.cooperators
        if respondent == Action.COOP:
            other_coop -= 1
        if other_coop >= (self.citizens - 1)/2:
            foes_action = Action.COOP
        else:
            foes_action = Action.DEF
        return self.matrix[respondent][foes_action]

    def analyse_case(self, accusing):
        self.cooperators = 0
        for action in accusing.values():
            if action == Action.COOP:
                self.cooperators += 1


if __name__ == '__main__':
    pm = PayoffMatrix(3, 0, 5, 1)
    pm.analyse_case({1: Action.COOP, 2: Action.DEF, 3: Action.DEF, 4: Action.COOP})
    print(pm.cooperators)
    print(pm.matrix)
    print(pm.is_prisoners_dilemma())
