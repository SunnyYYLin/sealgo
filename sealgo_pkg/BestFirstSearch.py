from SearchAlgo import Search
from Problem import SearchProblem, HeuristicSearchProblem, State, Action
from abc import abstractmethod
from queue import PriorityQueue, Queue, LifoQueue

class BestFirstSearch(Search):
    def __init__(self, problem:SearchProblem, eval_f = None):
        '''
        self.frontier = PriorityQueue(), 
        but actually it will be realized in different ways like stack, queue, etc.
        '''
        super().__init__(problem)
        self.reached = {}
        self.frontier = PriorityQueue()
        self.eval_f = eval_f
        init = problem.initial_state()
        self.frontier.put((self.eval_f(init), init))
        
    def search(self):
        while not self.frontier.empty():
            _, state = self.frontier.get()
            if self.problem.is_goal(state):
                return state
            self.reached[state] = state.cost
            for action in self.problem.actions(state):
                next_state = self.problem.result(state, action)
                if next_state not in self.reached or next_state.cost < self.reached[next_state]:
                    self.frontier.put((self.eval_f(next_state), next_state))

class BFS(BestFirstSearch):
    def __init__(self, problem:SearchProblem):
        super().__init__(problem, lambda x: x.cost)

    def search(self):
        return super().search()
    
if __name__ == '__main__':
    from ExampleProblem import EightQueens
    problem = EightQueens(8)
    algo = BFS(problem)
    print(algo.search())