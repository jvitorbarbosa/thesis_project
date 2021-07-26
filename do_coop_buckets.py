from simulator import cooperation_rates_per_policy
import sys
from policies import *
from rulers import *
from social_learners import *
import math
import numpy as np
import pandas as pd
from base import LearningParameters


# At command line it is required to give six parameters: p1 p2 p3 p4 p5 p6 p7
# p1: selects the game (npd, stag, risk)
# p2: selects the algorithm (nomem, major, selfless, level, allornone)
# p3: selects the policy (greedy, boltzmann, dyn_lin_grd, dyn_log_grd, lin_act_crt, std_pol)
# p4: selects the wealth multiplier (int)
# p5: number of rounds in each game (int)
# p6: number of citizens in the public good game (int)
# p7: identifier to put on the file name (string)
def main():
    game = None
    if sys.argv[1] == "npd":
        game = NPDRuler
    elif sys.argv[1] == "stag":
        game = ThresholdRuler
    elif sys.argv[1] == "risk":
        game = RiskyRuler
    else:
        print("Error: first parameter (game) not valid. Must be: npd, stag or risk.")
        return

    algorithm = None
    if sys.argv[2] == "nomem":
        algorithm = MemoryLess
    elif sys.argv[2] == "major":
        algorithm = MajorTDFour
    elif sys.argv[2] == "level":
        algorithm = LevelLearner
    elif sys.argv[2] == "selfless":
        algorithm = SelflessLearner
    elif sys.argv[2] == "allornone":
        algorithm = AllOrNone
    else:
        print("Error: second parameter (algorithm) not valid. Must be: nomem, major, selfless or level.")
        return

    buckets = None
    if sys.argv[3] == "greedy":
        buckets = [EpsilonGreedy(math.pow(10, (-1) * i)) for i in range(1, 7)]
    elif sys.argv[3] == "boltzmann":
        buckets = [Boltzmann(math.pow(10, i-2)) for i in range(4)]
    elif sys.argv[3] == "lin_act_crt":
        buckets = [ActorCriticLinear(i, LearningParameters().alpha) for i in [0.05, 0.1, 0.3, 0.5, 0.7, 0.9, 1]]
    elif sys.argv[3] == "dyn_lin_grd":
        buckets = [DynLinearEpsilonGreedy(i) for i in [0.001, 0.01, 0.1, 1]]
    elif sys.argv[3] == "dyn_log_grd":
        buckets = [DynLogEpsilonGreedy(i) for i in [0.001, 0.01, 0.1, 1]]
    elif sys.argv[3] == "std_pol":
        buckets = [EpsilonGreedy(0.001)]
    else:
        print("Error: third parameter (policy) not valid. Must be: greedy, boltzmann,\n"
              "dyn_lin_grd, dyn_log_grd, lin_act_crt or std_pol.")
        return

    multiplier = 2
    rounds = 100
    citizens = 5
    try:
        multiplier = int(sys.argv[4])
        rounds = int(sys.argv[5])
        citizens = int(sys.argv[6])
    except ValueError or TypeError:
        print("Error: fourth (wealth multiplier), fifth (number of rounds) and "
              "sixth (number of players) parameters must be integers.")
        return

    coop_rates = cooperation_rates_per_policy(algorithm, game(1, citizens, f=multiplier),
                                               20, buckets, iterations=rounds, show=True)

    file_name = "coop_" + sys.argv[1] + "_" + sys.argv[2] + "_" + sys.argv[3] + "_" + sys.argv[4] + \
                "_" + sys.argv[5] + "_" + sys.argv[6] + "_" + sys.argv[7] + ".txt"
    db = pd.DataFrame(data=np.array(coop_rates))
    db.to_csv(path_or_buf="raw/" + file_name)


main()
