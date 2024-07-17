from abc import ABC, abstractmethod
from .Problem import SearchProblem, Action
from typing import List

class Search(ABC):
    @abstractmethod
    def __init__(self, problem: SearchProblem) -> None:
        self.problem = problem
    
    @abstractmethod
    def search(self) -> List[List[Action]]:
        """
        Execute an uninformed search algorithm to find a solution to the given problem.
        Returns a solution or indicates failure.
        """
        pass