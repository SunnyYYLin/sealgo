from abc import ABC, abstractmethod
from typing import List

class State(ABC):
    '''
    __hash__: () -> int
    __eq__: (State) -> bool
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
    __hash__: () -> int
    __eq__: (Action) -> bool
    '''
    @abstractmethod
    def __hash__(self):
        pass
    
    @abstractmethod
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

class SearchProblem(ABC):
    '''
    initial_state: State
    actions: (State) -> list[Action]
    result: (State, Action) -> State
    is_goal: (State) -> bool
    action_cost: (State, Action) -> float
    '''
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

    def action_cost(self, s: State, action: Action) -> float:
        """Return the cost of taking action from state to another state."""
        return 1
    
class HeuristicSearchProblem(SearchProblem):
    """
    initial_state: State
    actions: (State) -> list[Action]
    result: (State, Action) -> State
    is_goal: (State) -> bool
    action_cost: (State, Action) -> float
    heuristic(State) -> float: the target function to MINIMIZE
    """
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