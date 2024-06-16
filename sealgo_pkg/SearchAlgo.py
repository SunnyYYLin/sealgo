from abc import ABC, abstractmethod
from Problem import SearchProblem

class Search(ABC):
    @abstractmethod
    def __init__(self, problem: SearchProblem):
        self.problem = problem
    
    @abstractmethod
    def search(self):
        """
        Execute an uninformed search algorithm to find a solution to the given problem.
        Returns a solution or indicates failure.
        """
        pass