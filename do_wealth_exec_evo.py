from simulator import pg_exec_evolution
import sys
from policies import *
from rulers import *
from social_learners import *
import numpy as np
import pandas as pd


# At command line it is required to give six parameters: p1 p2 p3 p4 p5 p6 p7
# p1: selects the game (npd, stag, risk)
# p2: selects the algorithm (nomem, major, selfless, level)
# p3: selects the policy (greedy, boltzmann, dyn_lin_grd, dyn_log_grd, lin_act_crt, std_pol)
# p4: selects the wealth multiplier (int)
# p5: number of games  (int)
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
    else:
        print("Error: second parameter (algorithm) not valid. Must be: nomem, major, selfless or level.")
        return

    policy = None
    if sys.argv[3] == "greedy":
        policy = EpsilonGreedy(0.01)
    elif sys.argv[3] == "boltzmann":
        policy = Boltzmann(1)
    elif sys.argv[3] == "lin_act_crt":
        policy = ActorCriticLinear(1)
    elif sys.argv[3] == "lin_act_crt-":
        policy = ActorCriticLinear(0.05)
    elif sys.argv[3] == "dyn_lin_grd":
        policy = DynLinearEpsilonGreedy(0.1)
    elif sys.argv[3] == "dyn_log_grd":
        policy = DynLogEpsilonGreedy(0.01)
    elif sys.argv[3] == "grd-":
        policy = EpsilonGreedy(0.001)
    elif sys.argv[3] == "grd--":
        policy = EpsilonGreedy(0.0001)
    else:
        print("Error: third parameter (policy) not valid. Must be: greedy, boltzmann,\n"
              "dyn_lin_grd, dyn_log_grd, lin_act_crt or std_pol.")
        return

    multiplier = 2
    n_games = 100
    citizens = 5
    try:
        multiplier = int(sys.argv[4])
        n_games = int(sys.argv[5])
        citizens = int(sys.argv[6])
    except ValueError or TypeError:
        print("Error: third (wealth multiplier), fourth (number of rounds) and "
              "fifth (number of players) parameters must be integers.")
        return

    str_changes = pg_exec_evolution(algorithm, game(1, citizens, f=multiplier),
                                        policy, 20, iterations=n_games, show=False)

    file_name = "pg_evo_" + sys.argv[1] + "_" + sys.argv[2] + "_" + sys.argv[3] + "_" + sys.argv[4] + \
                "_" + sys.argv[5] + "_" + sys.argv[6] + "_" + sys.argv[7] + ".txt"

    db = pd.DataFrame(data=np.array(str_changes))
    db.to_csv(path_or_buf="raw/" + file_name)


main()
