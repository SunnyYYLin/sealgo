from tests.queen import EightQueens
from sealgo.local_search import *
import numpy as np

if __name__ == '__main__':
    # test the eight queens problem
    problem = EightQueens()
    state = problem.initial_state()
    print(state)
    actions = problem.actions(state)
    print(actions)
    print(problem.result(state, actions[0]))
    print(problem.heuristic(state))
    
    # test local search
    hc = SimulatedAnnealing(problem)
    solution = hc.search()
    print(solution)