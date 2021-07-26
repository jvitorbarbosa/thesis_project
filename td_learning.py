from base import *


class TDOne(Player):

    def __init__(self, judge, policy, param):
        super().__init__(judge, param)
        self.q_values = [0, 0]  # First is cooperation and second is defection
        self.policy = policy
        self.next_action = Action.COOP

    def __str__(self):
        return "td1" + super().__str__()

    def act(self, condition=True):
        last_action = self.next_action
        self.next_action = self.policy.choose(self.q_values)
        return last_action

    def learn(self, actions):
        reward = super().learn(actions)
        action = actions[self.id]
        self.q_values[action] = self.q_values[action] + self.param.alpha * \
                                          ((reward + self.param.gamma * self.q_values[self.next_action])
                                           - self.q_values[action])


class TDTwo(Player):

    def __init__(self, judge, policy, param):
        super().__init__(judge, param)
        self.q_values = {Action.COOP: [0, 0], Action.DEF: [0, 0]}
        self.policy = policy
        self.next_action = Action.COOP
        self.state = Action.COOP
        self.next_state = Action.COOP

    def __str__(self):
        return "td2" + super().__str__()

    def act(self, condition=True):
        self.state = self.next_state
        self.next_state = self.next_action  # It is the last action taken
        self.next_action = self.policy.choose(self.q_values[self.next_state])
        return self.next_state

    def learn(self, actions):
        reward = super().learn(actions)
        action = actions[self.id]
        self.q_values[self.state][action] = self.q_values[self.state][action] + self.param.alpha * \
                                            ((reward + self.param.gamma * self.q_values[self.next_state][self.next_action])
                                             - self.q_values[self.state][action])


class TDFour(Player):

    def __init__(self, judge, policy, param):
        super().__init__(judge, param)
        self.q_values = {FourState.cc: [0, 0], FourState.cd: [0, 0], FourState.dc: [0, 0], FourState.dd: [0, 0]}
        self.policy = policy
        self.next_action = Action.COOP
        self.state = FourState.cc
        self.next_state = FourState.cc

    def __str__(self):
        return "td4" + super().__str__()

    def act(self, condition=True):
        return self.next_action

    def learn(self, actions):
        action = actions[self.id]
        foes_action = Action.DEF
        if list(actions.values()).count(Action.COOP) >= self.judge.citizens / 2:
            foes_action = Action.COOP
        self.next_state = action_to_statetd4(action, foes_action)  # Calculate s_t+1
        self.next_action = self.policy.choose(self.q_values[self.next_state])  # Calculate a_t+1
        reward = super().learn(actions)
        self.q_values[self.state][action] = self.q_values[self.state][action] + self.param.alpha * \
                                            ((reward + self.param.gamma * self.q_values[self.next_state][self.next_action])
                                             - self.q_values[self.state][action])
        self.state = self.next_state

    def strategy(self):
        s = "0000"
        order = {FourState.cc: 0, FourState.cd: 1, FourState.dc: 2, FourState.dd: 3}
        for state in self.q_values.keys():
            if self.q_values[state][Action.COOP] >= self.q_values[state][Action.DEF]:
                s = s[:order[state]] + str(Action.COOP.value) + s[order[state] + 1:]
        return s


if __name__ == '__main__':
    from rulers import PayoffMatrix
    td = TDFour(PayoffMatrix(3, 0, 5, 1), 0.01)
    td.q_values = {FourState.cc: [3, 1], FourState.cd: [1, 0], FourState.dc: [2, 1], FourState.dd: [2, 1]}
    print(td.strategy())
