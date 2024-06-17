from Problem import *
from SearchAlgo import Search
from abc import abstractmethod
        
class Minimax(Search):
    def __init__(self, problem: HeuristicSearchProblem, init: GameState, depth: int = 3):
        super().__init__(problem)
        self.state = init
        self.depth = depth
        
    def search(self) -> GameAction:
        def max_value(state, alpha, beta, depth) -> int:
            if depth == 0 or self.problem.is_goal(state):
                return self.problem.heuristic(state)
            v = float('-inf')
            for action in self.problem.actions(state):
                new_state = self.problem.result(state, action)
                v = max(v, min_value(new_state, alpha, beta, depth - 1))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(state, alpha, beta, depth) -> int:
            if depth == 0 or self.problem.is_goal(state):
                return self.problem.heuristic(state)
            v = float('inf')
            for action in self.problem.actions(state):
                new_state = self.problem.result(state, action)
                v = min(v, max_value(new_state, alpha, beta, depth - 1))
                if v <= alpha:
                    return v  # Alpha 剪枝
                beta = min(beta, v)
            return v

        best_score = float('-inf')
        best_action = None
        alpha = float('-inf')
        beta = float('inf')
        for action in self.problem.actions(self.state):
            new_state = self.problem.result(self.state, action)
            score = min_value(new_state, alpha, beta, self.depth - 1)
            if score > best_score:
                best_score = score
                best_action = action
                alpha = max(alpha, score)  # 更新 alpha 值
        return best_action
    
if __name__ == '__main__':
    from ExampleProblem import TicTacToe
    problem = TicTacToe()
    init = problem.initial_state()
    print(init)
    minimax = Minimax(problem, init)
    print(minimax.search())