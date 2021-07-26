from simulator import cooperation_rates_per_param
import sys
from policies import *
from rulers import *
from social_learners import *
import numpy as np
import pandas as pd


# At command line it is required to give six parameters: p1 p2 p3 p4 p5 p6 p7
# p1: selects the parameter to variate (alpha, gamma)
# p2: selects the game (npd, stag, risk)
# p3: selects the algorithm (nomem, major, selfless, level)
# p4: selects the policy (greedy, boltzmann, dyn_lin_grd, dyn_log_grd, lin_act_crt, std_pol)
# p5: selects the wealth multiplier (int)
# p6: number of rounds in each game (int)
# p7: number of citizens in the public good game (int)
# p8: identifier to put on the file name (string)
def main():
    parameter = sys.argv[1]
    if parameter not in ['alpha', 'gamma']:
        print("Error: first parameter not valid. Must be: alpha or gamma.")
        return

    game = None
    if sys.argv[2] == "npd":
        game = NPDRuler
    elif sys.argv[2] == "stag":
        game = ThresholdRuler
    elif sys.argv[2] == "risk":
        game = RiskyRuler
    else:
        print("Error: second parameter (game) not valid. Must be: npd, stag or risk.")
        return

    algorithm = None
    if sys.argv[3] == "nomem":
        algorithm = MemoryLess
    elif sys.argv[3] == "major":
        algorithm = MajorTDFour
    elif sys.argv[3] == "level":
        algorithm = LevelLearner
    elif sys.argv[3] == "selfless":
        algorithm = SelflessLearner
    else:
        print("Error: third parameter (algorithm) not valid. Must be: nomem, major, selfless or level.")
        return

    policy = None
    if sys.argv[4] == "greedy":
        policy = EpsilonGreedy(0.01)
    elif sys.argv[4] == "boltzmann":
        policy = Boltzmann(0.01)
    elif sys.argv[4] == "lin_act_crt":
        policy = ActorCriticLinear(0.05)
    elif sys.argv[4] == "dyn_lin_grd":
        policy = DynLinearEpsilonGreedy(0.01)
    elif sys.argv[4] == "dyn_log_grd":
        policy = DynLogEpsilonGreedy(0.001)
    elif sys.argv[4] == "grd-":
        policy = EpsilonGreedy(0.001)
    elif sys.argv[4] == "grd--":
        policy = EpsilonGreedy(0.0001)
    else:
        print("Error: fourth parameter (policy) not valid. Must be: greedy, boltzmann,\n"
              "dyn_lin_grd, dyn_log_grd, lin_act_crt or std_pol.")
        return

    multiplier = 2
    rounds = 100
    citizens = 5
    try:
        multiplier = int(sys.argv[5])
        rounds = int(sys.argv[6])
        citizens = int(sys.argv[7])
    except ValueError or TypeError:
        print("Error: fifth (wealth multiplier), sixth (number of rounds) and "
              "seventh (number of players) parameters must be integers.")
        return

    coop_rates = cooperation_rates_per_param(algorithm, game(1, citizens, f=multiplier),
                                               20, policy, param=parameter, iterations=rounds, show=True)

    file_name = "coop_" + sys.argv[1] + "_" + sys.argv[2] + "_" + sys.argv[3] + "_" + sys.argv[4] + \
                "_" + sys.argv[5] + "_" + sys.argv[6] + "_" + sys.argv[7] + "_" + sys.argv[8] + ".txt"
    db = pd.DataFrame(data=np.array(coop_rates))
    db.to_csv(path_or_buf="raw/" + file_name)


main()
