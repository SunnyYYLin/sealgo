from tests.queen import EightQueens
from sealgo.local_search import *

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
    # hc = HillClimbing(problem)
    # solution = hc.search()
    # print(solution)
    
    # shc = StochasticHillClimbing(problem)
    # solution = shc.search()
    # print(solution)
    
    # fchc = FirstChoiceHillClimbing(problem)
    # solution = fchc.search()
    # print(solution)
    
    # sa = SimulatedAnnealing(problem)
    # solution = sa.search()
    # print(solution)
    
    rr = RandomRestart(problem, HillClimbing, max_iter=100, max_restarts=100)
    solution = rr.search()
    print(solution)