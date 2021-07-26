import sys
from social_learners import *
from simulator import strategies_learned
from policies import EpsilonGreedy
from rulers import NPDRuler
import numpy as np
import pandas as pd


# At command line it is required to give four parameters: p1 p2 p3 p4
# p1: selects the algorithm (nomem, major, level)
# p2: selects the wealth multiplier (int)
# p3: number of rounds in each game (int)
# p4: identifier to put on the file name (string)
def main():
    algorithm = None
    if sys.argv[1] == "nomem":
        algorithm = MemoryLess
    elif sys.argv[1] == "major":
        algorithm = MajorTDFour
    elif sys.argv[1] == "level":
        algorithm = LevelLearner
    else:
        print("Error: first parameter (algorithm) not valid. Must be: nomem, major or level.")
        return

    multiplier = 2
    rounds = 100
    try:
        multiplier = int(sys.argv[2])
        rounds = int(sys.argv[3])
    except ValueError or TypeError:
        print("Error: second (wealth multiplier) and third (number of rounds) parameters must be integers.")
        return

    strategies = strategies_learned(MajorTDFour, NPDRuler(1, 5, f=multiplier),
                                    EpsilonGreedy(0.001), 20, iterations=rounds)

    file_name = "strategies_" + sys.argv[1] + "_" + sys.argv[2] + "_" + sys.argv[3] + "_" + sys.argv[4] + ".txt"
    db = pd.DataFrame(data=np.array(strategies))
    db.to_csv(path_or_buf="raw/" + file_name)


main()
