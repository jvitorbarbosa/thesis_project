from base import *
import random


class AlwaysCoop(Player):

    def __str__(self):
        return "allc"

    def act(self):
        return Action.COOP


class AlwaysDef(Player):

    def __str__(self):
        return "alld"

    def act(self):
        return Action.DEF


class TitForTat(Player):

    def __str__(self):
        return "tft"

    def __init__(self, judge):
        super().__init__(judge)
        self.last_foes_action = Action.COOP

    def act(self):
        return self.last_foes_action

    def learn(self, actions):
        super().learn(actions)
        cooperators = 0
        for num_id, act in actions.items():
            if num_id != self.id and act == Action.COOP:
                cooperators += 1
        if cooperators >= (self.judge.citizens - 1)/2:
            self.last_foes_action = Action.COOP
        else:
            self.last_foes_action = Action.DEF


class Alternate(Player):

    def __str__(self):
        return "alternate"

    def __init__(self, judge):
        super().__init__(judge)
        self.last_action = Action.COOP

    def act(self):
        return Action(not self.last_action)

    def learn(self, actions):
        super().learn(actions)
        self.last_action = actions[self.ID]


class Reactive(TitForTat):

    def __str__(self):
        return "reactive_" + str(int(100*self.p)) + "_" + str(int(100*self.q))

    def __init__(self, judge, p, q):
        super().__init__(judge)
        self.p = p
        self.q = q
        self.last_foes_action = Action.COOP

    def act(self):
        threshold = random.random()
        if self.last_foes_action == Action.COOP and threshold < self.p:
            return Action.COOP
        elif self.last_foes_action == Action.DEF and threshold < self.q:
            return Action.COOP
        return Action.DEF

    def learn(self, actions):
        super().learn(actions)


class TitForTwoTat(TitForTat):

    def __str__(self):
        return "tf2t"

    def __init__(self, judge):
        super().__init__(judge)
        self.list_foes_action = [Action.COOP, Action.COOP]

    def act(self):
        if self.list_foes_action[-1] == self.list_foes_action[-2] == Action.DEF:
            return Action.DEF
        return Action.COOP

    def learn(self, actions):
        super().learn(actions)
        self.list_foes_action.append(self.last_foes_action)


class WinStayLooseShift(TitForTat):

    def __str__(self):
        return "wsls"

    def __init__(self, judge):
        super().__init__(judge)
        self.last_foes_action = Action.COOP
        self.last_action = Action.COOP

    def act(self):
        if self.last_foes_action == Action.DEF:
            return Action(not self.last_action)
        return self.last_action

    def learn(self, actions):
        super().learn(actions)
        self.last_action = actions[self.id]


class MemoryOne(Player):

    def __str__(self):
        return "mem_" + self.ms.name

    def __init__(self, judge, ms, epsilon):
        super().__init__(judge)
        self.epsilon = epsilon
        self.state = FourState.cc
        self.ms = ms
        self.rules = memory_state_to_rule(ms)

    def act(self):
        if random.random() < self.epsilon:
            return Action(not self.rules[self.state])
        return self.rules[self.state]

    def learn(self, actions):
        super().learn(actions)
        cooperators = 0
        for num_id, act in actions.items():
            if num_id != self.id and act == Action.COOP:
                cooperators += 1
        if cooperators >= (self.judge.citizens - 1) / 2:
            foes_action = Action.COOP
        else:
            foes_action = Action.DEF
        self.state = action_to_statetd4(actions[self.id], foes_action)


if __name__ == '__main__':
    # p = TitForTwoTat()
    # for i in range(10):
    #     if i < 4:
    #         p.last_foes_action = Action.COOP
    #     else:
    #         p.last_foes_action = Action.DEF
    #     print(p.list_foes_action)
    #     print(p.act())
    
    input = [Action.COOP, Action.COOP, Action.DEF, Action.COOP, Action.DEF, Action.DEF]
    p = WinStayLooseShift()
    for i in input:
        print(p.act())
        p.last_foes_action = i
