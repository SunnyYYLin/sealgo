from abc import abstractmethod
from .SearchAlgo import GlobalSearch
from .Problem import HeuristicSearchProblem, State, Action
import diagrams as diag

class AndOrTreeSearch(GlobalSearch):
    def __init__(self, problem: HeuristicSearchProblem):
        super().__init__(problem)
        
    def __copy__(self):
        return AndOrTreeSearch(self.problem)

    def search(self, is_max):
        if self.problem.is_goal(self.state):
            return self.problem.heuristic(self.state)
        
        best_value = float('-inf') if is_max else float('inf')
        best_action = None
        for action in self.problem.actions(self.state):
            # Apply the action to the state
            new_state = self.problem.result(self.state, action)
            # Toggle the player
            successor = self.__copy__()
            value = successor.search(not is_max)
            # Maximizing player
            if is_max and value > best_value:
                best_value = value
                self.state = self.problem.result(self.state, action)
                self += self.problem.action_cost(self.state, action)
            # Minimizing player
            elif not is_max and value < best_value:
                best_value = value
                best_action = action

        # If it's a leaf node, return the heuristic value, else return the action
        return best_value if best_action is None else best_action
    
    def draw_tree(self):
        