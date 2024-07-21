from .Problem import SearchProblem
from .Search import Search

class MCTS(Search):
    def __init__(self, problem: SearchProblem, max_iter: int, max_time: float, max_depth: int, exploration_weight: float):
        super().__init__(problem)
        self.max_iter = max_iter
        self.max_time = max_time
        self.max_depth = max_depth
        self.exploration_weight = exploration_weight

    def search(self):
        pass