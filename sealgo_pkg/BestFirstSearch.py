from SearchAlgo import Search
from Problem import SearchProblem, HeuristicSearchProblem, State, Action
from abc import abstractmethod
from queue import PriorityQueue, Queue, LifoQueue

class BestFirstSearch(Search):
    def __init__(self, problem:SearchProblem, eval_f = lambda x: x.cost, qtype = PriorityQueue):
        '''
        self.frontier = PriorityQueue(), 
        but actually it will be realized in different ways like stack, queue, etc.
        '''
        super().__init__(problem)
        self.reached = {}
        self.qtype = qtype
        self.frontier = self.qtype()
        self.eval_f = eval_f
        init = problem.initial_state()
        if qtype == Queue or qtype == LifoQueue:
            self.frontier.put(init)
        elif qtype == PriorityQueue:
            self.frontier.put((self.eval_f(init), init))
        else:
            raise ValueError('Invalid queue type.')
        
    def search(self, only_one = True):
        if not only_one:
            goals = []
        while not self.frontier.empty():
            if self.qtype == PriorityQueue:
                state = self.frontier.get()[1]
            else:
                state = self.frontier.get()
            if self.problem.is_goal(state):
                if only_one:
                    return state
                goals.append(state)
                # print(f'Goal:\n{state}\n{state.cost}\n')
            self.reached[state] = state.cost
            # print(f'Reached:\n{state}\n{state.cost}\n')
            for action in self.problem.actions(state):
                next_state = self.problem.result(state, action)
                if next_state not in self.reached or next_state.cost < self.reached[next_state]:
                    if self.qtype == PriorityQueue:
                        self.frontier.put((self.eval_f(next_state), next_state))
                    else:
                        self.frontier.put(next_state)
        return goals

class BFS(BestFirstSearch):
    def __init__(self, problem:SearchProblem):
        super().__init__(problem, eval_f = lambda x: x.cost, qtype = Queue)
    
class DFS(BestFirstSearch):
    def __init__(self, problem:SearchProblem, max_depth = 1000):
        super().__init__(problem, eval_f = lambda x: -x.cost, qtype = LifoQueue)
        
class Dijkstra(BestFirstSearch):
    def __init__(self, problem:SearchProblem):
        super().__init__(problem, eval_f = lambda x: x.cost, qtype = PriorityQueue)
        
class GBFS(BestFirstSearch):
    def __init__(self, problem:HeuristicSearchProblem):
        super().__init__(problem, eval_f = lambda x: problem.heuristic(x), qtype = PriorityQueue)
        
class AStar(BestFirstSearch):
    def __init__(self, problem:HeuristicSearchProblem, weight:float=1):
        super().__init__(problem, eval_f = lambda x: x.cost+weight*problem.heuristic(x), qtype = PriorityQueue)
        
class 
    
if __name__ == '__main__':
    from ExampleProblem import EightQueens
    problem = EightQueens(10)
    algo = AStar(problem)
    print(algo.search(False))