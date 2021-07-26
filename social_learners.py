from td_learning import TDFour
from base import *


class MemoryLess(Player):
    def __init__(self, judge, policy, money, param):
        super().__init__(judge, param)
        self.total_reward = money
        self.starting_amount = money
        self.q_values = {"s0": [0, 0]}  # First is cooperation and second is defection
        self.policy = policy
        self.next_action = Action.COOP

    def __str__(self):
        return "noMem" + super().__str__()

    def act(self, is_learning=True):
        if is_learning:
            return self.next_action
        else:
            return self.policy.choose("s0", self.q_values, self.total_reward - self.judge.payment)

    def learn(self, actions):
        reward = super().learn(actions)
        action = actions[self.id]
        self.next_action = self.policy.choose("s0", self.q_values, self.total_reward - self.judge.payment)
        self.q_values["s0"][action] = self.q_values["s0"][action] + self.param.alpha * \
                                          ((reward + self.param.gamma * self.q_values["s0"][self.next_action])
                                           - self.q_values["s0"][action])

    def strategy(self):
        if self.q_values["s0"][Action.COOP] >= self.q_values["s0"][Action.DEF]:
            return str(Action.COOP.value)
        else:
            return str(Action.DEF.value)


class LevelLearner(Player):

    def __init__(self, judge, policy, money, param):
        super().__init__(judge, param)
        self.total_reward = money
        self.starting_amount = money
        self.q_values = {}
        for i in range(judge.citizens + 1):
            self.q_values[self.get_state(Action.COOP, i)] = [0, 0]
            self.q_values[self.get_state(Action.DEF, i)] = [0, 0]
        self.policy = policy
        self.next_action = Action.COOP
        self.state = self.get_state(Action.COOP, judge.citizens)
        self.next_state = self.get_state(Action.COOP, judge.citizens)

    def __str__(self):
        return "levelPlayer" + super().__str__()

    def act(self, is_learning=True):
        if is_learning:
            return self.next_action
        else:
            return self.policy.choose(self.next_state, self.q_values, self.total_reward - self.judge.payment)

    def learn(self, actions):
        number_of_cooperators = list(actions.values()).count(Action.COOP)
        action = actions[self.id]
        self.judge.analyse_case(actions)
        self.next_state = self.get_state(action, number_of_cooperators)  # Calculate s_t+1
        self.next_action = self.policy.choose(self.next_state, self.q_values, self.total_reward - self.judge.payment)
        reward = super().learn(actions)
        self.q_values[self.state][action] = self.q_values[self.state][action] + self.param.alpha * \
                                            ((reward + self.param.gamma * self.q_values[self.next_state][self.next_action])
                                             - self.q_values[self.state][action])
        self.state = self.next_state

    def receive_consequences(self, actions):
        number_of_cooperators = list(actions.values()).count(Action.COOP)
        action = actions[self.id]
        self.next_state = self.get_state(action, number_of_cooperators)
        return super().receive_consequences(actions)

    def strategy(self):
        s = ""
        order = [LevelLearner.get_state(Action.COOP, n1) for n1 in range(self.judge.citizens)] \
              + [LevelLearner.get_state(Action.DEF, n2) for n2 in range(self.judge.citizens)]
        for state in order:
            if state in self.q_values.keys():
                if self.q_values[state][Action.COOP] >= self.q_values[state][Action.DEF]:
                    s += str(Action.COOP.value)
                else:
                    s += str(Action.DEF.value)
            else:
                s += "-"
        return s

    @staticmethod
    def get_state(action, number_of_cooperators):
        return action.name + str(number_of_cooperators)


class SelflessLearner(LevelLearner):

    @staticmethod
    def get_state(action, number_of_cooperators):
        return str(number_of_cooperators)

    def strategy(self):
        s = ""
        order = [SelflessLearner.get_state(Action.COOP, n) for n in range(self.judge.citizens + 1)]
        for state in order:
            if state in self.q_values.keys():
                if self.q_values[state][Action.COOP] >= self.q_values[state][Action.DEF]:
                    s += str(Action.COOP.value)
                else:
                    s += str(Action.DEF.value)
            else:
                s += str(Action.COOP.value)
        return s


class MajorTDFour(TDFour):

    def __init__(self, judge, policy, money, param):
        super().__init__(judge, policy, param)
        self.total_reward = money
        self.starting_amount = money

    def __str__(self):
        return "MajorTD4" + super().__str__()

    def act(self, is_learning=True):
        if is_learning:
            return self.next_action
        else:
            return self.policy.choose(self.next_state, self.q_values, self.total_reward - self.judge.payment)

    def learn(self, actions):
        self.judge.analyse_case(actions)
        foes_action = Action.DEF
        if list(actions.values()).count(Action.COOP) >= self.judge.citizens / 2:
            foes_action = Action.COOP
        self.next_state = action_to_statetd4(actions[self.id], foes_action)  # Calculate s_t+1
        self.next_action = self.policy.choose(self.next_state, self.q_values, self.total_reward - self.judge.payment)
        reward = Player.learn(self, actions)
        self.q_values[self.state][actions[self.id]] = self.q_values[self.state][actions[self.id]] + self.param.alpha * \
                                            ((reward + self.param.gamma * self.q_values[self.next_state][self.next_action])
                                             - self.q_values[self.state][actions[self.id]])
        self.state = self.next_state

    def receive_consequences(self, actions):
        foes_action = Action.DEF
        if list(actions.values()).count(Action.COOP) >= self.judge.citizens / 2:
            foes_action = Action.COOP
        self.next_state = action_to_statetd4(actions[self.id], foes_action)
        return Player.receive_consequences(self, actions)


class AllOrNone(Player):
    def __init__(self, judge, policy, money, param, threshold=0.5):
        super().__init__(judge, param)
        self.total_reward = money
        self.starting_amount = money
        self.q_values = {"0": [0, 0], "<": [0, 0], ">": [0, 0], "N": [0, 0]}  # First is cooperation and second is defection
        self.policy = policy
        self.next_action = Action.COOP
        self.state = self.get_state(Action.COOP, judge.citizens)
        self.next_state = self.get_state(Action.COOP, judge.citizens)
        self.threshold = threshold

    def get_state(self, action, number_of_cooperators):
        if number_of_cooperators == self.judge.citizens:
            return "N"
        elif number_of_cooperators == 0:
            return "0"
        elif number_of_cooperators <= self.threshold * self.judge.citizens:
            return "<"
        else:
            return ">"

    def act(self, is_learning=True):
        if is_learning:
            return self.next_action
        else:
            return self.policy.choose(self.next_state, self.q_values, self.total_reward - self.judge.payment)

    def learn(self, actions):
        number_of_cooperators = list(actions.values()).count(Action.COOP)
        action = actions[self.id]
        self.judge.analyse_case(actions)
        self.next_state = self.get_state(action, number_of_cooperators)  # Calculate s_t+1
        self.next_action = self.policy.choose(self.next_state, self.q_values, self.total_reward - self.judge.payment)
        reward = super().learn(actions)
        self.q_values[self.state][action] = self.q_values[self.state][action] + self.param.alpha * (
                                                (reward +
                                                 self.param.gamma * self.q_values[self.next_state][self.next_action]) -
                                                 self.q_values[self.state][action])
        self.state = self.next_state

    def receive_consequences(self, actions):
        number_of_cooperators = list(actions.values()).count(Action.COOP)
        action = actions[self.id]
        self.next_state = self.get_state(action, number_of_cooperators)
        return super().receive_consequences(actions)
