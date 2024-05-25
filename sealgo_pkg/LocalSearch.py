from abc import abstractmethod
from collections.abc import Callable
from .SearchAlgo import Search
from .Problem import SearchProblem, State, Action
import random
from math import exp

class LocalSearch(Search):
    @abstractmethod
    def __init__(self, problem: SearchProblem, max_iter: int = 1000):
        super().__init__(problem)
        self.max_iter = max_iter
        
    @abstractmethod
    def search(self) -> bool:
        """
        Execute a local search algorithm to find a solution to the given problem.
        Returns a solution or indicates failure.
        """
        pass
    
class HillClimbing(LocalSearch):
    def __init__(self, problem: SearchProblem, max_iter: int = 1000):
        """
        Initialize the hill climbing search algorithm with the given problem and maximum number of iterations.
        """
        super().__init__(problem, max_iter)
    
    def climb(self, actions: list[Action]) -> tuple[Action, bool]:
        """Execute a hill climbing search algorithm pattern to return an action and decide whether to end."""
        action = min(actions, key=lambda n: self.problem.heuristic(self.problem.result(self.state, n)))
        is_end = self.problem.heuristic(self.problem.result(self.state, action)) >= self.problem.heuristic(self.state)
        return action, is_end
    
    def search(self):
        """
        Execute a hill climbing search algorithm to find a solution to the given problem.
        Returns a solution or indicates failure.
        """
        for _ in range(self.max_iter):
            if self.problem.is_goal(self.state):
                break
            actions = self.problem.actions(self.state)
            if not actions:
                break
            chosen_action, is_end = self.climb(actions)
            if is_end:
                break
            if not chosen_action:
                continue
            self.state = self.problem.result(self.state, chosen_action)
            self.cost += self.problem.action_cost(self.state, chosen_action)
        return self.problem.is_goal(self.state)
    
class StochasticHillClimbing(HillClimbing):
    def __init__(self, problem: SearchProblem, max_iter: int = 1000, p: Callable = lambda x: 0.5):
        """
        Initialize the stochastic hill climbing search algorithm with the given problem, maximum number of iterations, and probability function.
        """
        super().__init__(problem, max_iter)
        self.p = p
        
    def climb(self, actions: list[Action]) -> tuple[Action, bool]:
        action = random.choice(actions)
        slope = self.problem.heuristic(self.problem.result(self.state, action)) - self.problem.heuristic(self.state)
        if slope >= 0:
            prob = self.p(slope)
            if random.random() > prob:
                print(f"reject: {slope}")
                action = None
        return action, False
    
class FirstChoiceHillClimbing(StochasticHillClimbing):
    def __init__(self, problem: SearchProblem, max_iter: int = 1000):
        """
        Initialize the first-choice hill climbing search algorithm with the given problem and maximum number of iterations.
        """
        super().__init__(problem, max_iter, p=lambda x: 1 if x > 0 else 0)
        
class SimulatedAnnealing(StochasticHillClimbing):
    def __init__(self, problem: SearchProblem, max_iter: int = 1000, T_0: float = 1.0, alpha: float = 0.9):
        """
        Initialize the simulated annealing search algorithm with the given problem, maximum number of iterations, probability function, and temperature.
        """
        super().__init__(problem, max_iter, self.p)
        self.T_0 = T_0
        self.T = self.T_0
        self.alpha = alpha
        
    def p(self, slope: float) -> float:
        p_annealing = 1 if slope > 0 else 1/(1 + exp(-slope/self.T))
        self.T = self.T_0 * self.alpha
        return p_annealing
        
class RandomRestart(LocalSearch):
    def __init__(self, problem: SearchProblem, algorithm: LocalSearch, max_iter: int = 1000, restarts: int = 10):
        """
        Initialize the random restart search algorithm with the given problem, maximum number of iterations, and number of restarts.
        """
        super().__init__(problem, max_iter)
        self.restarts = restarts
        self.algorithm = algorithm
        self.algorithm.max_iter = max_iter
        
    def search(self):
        """
        Execute a random restart on a certain search algorithm to find a solution to the given problem.
        """
        if self.problem != self.algorithm.problem:
            raise ValueError("The problem of the algorithm must be the same as the problem of the search.")

        for _ in range(self.restarts):
            self.algorithm.state = self.problem.initial_state()
            self.algorithm.cost = 0
            self.algorithm.search()
            if self.problem.is_goal(self.algorithm.state) and self.algorithm.cost < self.cost:
                self.state = self.algorithm.state
                self.cost = self.algorithm.cost
                
        return self.problem.is_goal(self.state)