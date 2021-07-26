from enum import IntEnum
from enum import Enum
import pandas as pd


class Action(IntEnum):
    DEF = 0
    COOP = 1


class LearningParameters:
    gamma = 0.9
    alpha = 0.05


class FourState(IntEnum):
    dd = str(int(Action.DEF)) + str(int(Action.DEF))
    dc = str(int(Action.DEF)) + str(int(Action.COOP))
    cd = str(int(Action.COOP)) + str(int(Action.DEF))
    cc = str(int(Action.COOP)) + str(int(Action.COOP))


def action_to_statetd4(action1, action2):
    return FourState(int(str(int(action1)) + str(int(action2))))


def memory_state_to_rule(ms):
    return {FourState.cc: Action(int(ms.value[0])),
            FourState.cd: Action(int(ms.value[1])),
            FourState.dc: Action(int(ms.value[2])),
            FourState.dd: Action(int(ms.value[3]))}


class MemoryState(Enum):
    S00 = "0000"
    S01 = "0001"
    S02 = "0010"
    S03 = "0011"
    S04 = "0100"
    S05 = "0101"
    S06 = "0110"
    S07 = "0111"
    S08 = "1000"
    S09 = "1001"
    S10 = "1010"
    S11 = "1011"
    S12 = "1100"
    S13 = "1101"
    S14 = "1110"
    S15 = "1111"

    def __eq__(self, other):
        if int(self.value, 2) == int(other.value, 2):
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if int(self.value, 2) < int(other.value, 2):
            return True
        return False

    def __gt__(self, other):
        if int(self.value, 2) > int(other.value, 2):
            return True
        return False

    def __ge__(self, other):
        return not self.__lt__(other)

    def __le__(self, other):
        return not self.__gt__(other)


class Player:
    ID = 0

    def __init__(self, judge, param):
        self.judge = judge
        self.total_reward = 0
        self.starting_amount = 0
        self.num_trials = 0
        self.id = Player.ID
        self.param = param
        Player.ID += 1

    def __str__(self):
        return ":" + str(self.id)

    def act(self, condition=True):
        print("Not Implemented")

    def learn(self, actions):
        reward = self.judge.sentence(actions[self.id])
        self.total_reward += reward
        self.num_trials += 1
        return reward

    def receive_consequences(self, actions):
        self.judge.analyse_case(actions)
        reward = self.judge.sentence(actions[self.id])
        self.total_reward += reward
        self.num_trials += 1
        return reward

    def expected_reward(self):
        return self.total_reward / self.num_trials

    def reset(self):
        self.total_reward = self.starting_amount
        self.num_trials = 0

    def strategy(self):
        return "None"


class Judge:

    def __init__(self, payment, citizens):
        self.payment = payment
        self.citizens = citizens

    def sentence(self, respondent):
        print("Not Implemented")

    def analyse_case(self, accusing):
        print("Not Implemented")


class Policy:

    def __str__(self):
        print("Not Implemented")

    def choose(self, state, value_table, credit):
        print("Not Implemented")


def compress_data(name, is_group_bars=True):
    raw_data = []
    for i in range(1, 5):
        raw_data.append(pd.read_csv("raw/" + name + str(i) + ".txt").iloc[:, 1:].values)
    data = []
    for label in range(len(raw_data[0])):
        line = []
        for part in range(len(raw_data)):
            line += list(raw_data[part][label])
        if is_group_bars:
            data.append(line)
        else:
            data.append([line])
    return data


if __name__ == '__main__':
    # print(MemoryState.S0.value)
    # # print(MemoryState.value)
    # print(MemoryState("1010"))
    # print(MemoryState('{:b}'.format(10)))
    # print(int(MemoryState.S0.value, 2))
    # print(MemoryState.S3 > MemoryState.S12)
    # print(MemoryState.S3 != MemoryState.S12)
    # print(MemoryState.S3 < MemoryState.S12)
    # print(MemoryState.S3 >= MemoryState.S12)
    # print(MemoryState.S3 <= MemoryState.S12)
    print(Player(1), Player(2), Player(3))


