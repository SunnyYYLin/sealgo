from abc import ABC, abstractmethod
from .Problem import SearchProblem

class Search(ABC):
    @abstractmethod
    def __init__(self, problem: SearchProblem):
        self.problem = problem
        self.state = problem.initial_state()
        self.cost = 0
    
    @abstractmethod
    def search(self):
        """
        Execute an uninformed search algorithm to find a solution to the given problem.
        Returns a solution or indicates failure.
        """
        pass
    
class GlobalSearch(Search):
    @abstractmethod
    def __init__(self, problem: SearchProblem):
        super().__init__(problem)
    
    @abstractmethod
    def search(self):
        """
        Execute a global search algorithm to find a solution to the given problem.
        Returns a solution or indicates failure.
        """
        pass