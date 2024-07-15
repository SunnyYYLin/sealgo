from abc import ABC, abstractmethod
from typing import List

class State(ABC):
    '''
    Represents a state in the problem domain.

    Attributes:
        cost (int): The cost associated with the state.

    Methods:
        __hash__(): Computes the hash value of the state.
        __eq__(other): Compares the state with another state for equality.
    '''
    def __init__(self, cost:int=0):
        self.cost = cost
        
    @abstractmethod
    def __hash__(self):
        pass
    
    @abstractmethod
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
    
class Action(ABC):
    '''
    
    '''
    @abstractmethod
    def __hash__(self):
        pass
    
    @abstractmethod
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

class SearchProblem(ABC):
    """
    An abstract class representing a search problem.
    
    Methods:
        initial_state(self) -> State: Return the initial state from which the problem is to be solved.
        actions(self, state: State) -> list: Return a list of actions that can be executed in the given state.
        result(self, state: State, action: Action) -> State: Return the state that results from executing a given action in the given state.
        is_goal(self, state: State) -> bool: Check if the given state is a goal state.
        action_cost(self, s: State, action: Action) -> int|float: Return the cost of taking action from state to another state.
    """
    
    @abstractmethod
    def initial_state(self) -> State:
        """Return the initial state from which the problem is to be solved."""
        pass

    @abstractmethod
    def actions(self, state: State) -> list:
        """Return a list of actions that can be executed in the given state."""
        pass

    @abstractmethod
    def result(self, state: State, action: Action) -> State:
        """Return the state that results from executing a given action in the given state."""
        if not action:
            return state
        pass

    @abstractmethod
    def is_goal(self, state: State) -> bool:
        """Check if the given state is a goal state."""
        pass

    def action_cost(self, s: State, action: Action) -> int|float:
        """Return the cost of taking action from state to another state."""
        return 1
    
class HeuristicSearchProblem(SearchProblem):
    '''
    A class representing a heuristic search problem.
    
    Methods:
        initial_state(self) -> State: Return the initial state from which the problem is to be solved.
        actions(self, state: State) -> list: Return a list of actions that can be executed in the given state.
        result(self, state: State, action: Action) -> State: Return the state that results from executing a given action in the given state.
        is_goal(self, state: State) -> bool: Check if the given state is a goal state.
        action_cost(self, s: State, action: Action) -> int|float: Return the cost of taking action from state to another state.
        heuristic(state: State) -> float: Returns the heuristic value of the given state.
    '''
    @abstractmethod
    def heuristic(self, state: State) -> float:
        """Return the heuristic value of the given state."""
        pass
    
class UncertainSearchProblem(SearchProblem):
    @abstractmethod
    def result(self, state: State, action: Action) -> List[tuple[State, float]]:
        pass
    
class GameState(State):
    @abstractmethod
    def __init__(self, cost: int = 0, to_move: str = None):
        super().__init__(cost)
        self.to_move = to_move
        
class GameAction(Action):
    @abstractmethod
    def __init__(self, cost: int = 0, player: str = None):
        super().__init__(cost)
        self.player = player