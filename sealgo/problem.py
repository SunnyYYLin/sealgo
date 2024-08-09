from abc import ABC, abstractmethod
from enum import Enum, auto

class State(ABC):
    '''
    Represents a state in the problem domain.

    Methods:
        __hash__(): Computes the hash value of the state (Must be realized in subclasses).
        __eq__(other): Compares the state with another state for equality.
        __lt__(other): Compares the state with another state for less than.
    ''' 
    @abstractmethod
    def __hash__(self) -> int:
        pass
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and hash(self) == hash(other)
    
    def __lt__(self, other: "State") -> bool:
        return hash(self) < hash(other)
    
class Action(ABC):
    """
    Represents an action that can be taken in the problem domain.
    """
    @abstractmethod
    def __hash__(self) -> int:
        pass
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and hash(self) == hash(other)
    
    def __lt__(self, other: "Action") -> bool:
        return hash(self) < hash(other)
    
class Stay(Action):
    def __hash__(self) -> int:
        return 0
    
STAY = Stay()

class SearchProblem(ABC):
    """
    An abstract class representing a search problem.
    
    Methods(must be realized in subclasses):
        initial_state(self) -> State: Return the initial state from which the problem is to be solved.
        actions(self, state: State) -> list[Action]: Return a list of actions that can be executed in the given state.
        result(self, state: State, action: Action) -> State: Return the state that results from executing a given action in the given state.
        is_goal(self, state: State) -> bool: Check if the given state is a goal state.
        action_cost(self, s: State, action: Action) -> int|float: Return the cost of taking action from state to another state.
    """
    
    @abstractmethod
    def initial_state(self) -> State:
        """Return the initial state from which the problem is to be solved."""
        pass

    @abstractmethod
    def actions(self, state: State) -> list[Action]:
        """Return a list of actions that can be executed in the given state."""
        pass

    @abstractmethod
    def result(self, state: State, action: Action) -> State:
        """Return the state that results from executing a given action in the given state.
        If action == Action.STAY, return the same state.
        """
        pass

    @abstractmethod
    def is_goal(self, state: State) -> bool:
        """Check if the given state is a goal state."""
        pass

    @abstractmethod
    def action_cost(self, s: State, action: Action) -> int|float:
        """Return the cost of taking action from state to another state."""
        return 1
    
class HeuristicSearchProblem(SearchProblem):
    '''
    A class representing a heuristic search problem.
    
    Methods(must be realized in subclasses):
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
    
class BiSearchProblem(SearchProblem):
    """
    A class representing a bidirectional search problem.
    
    Methods(must be realized in subclasses):
        initial_state(self) -> State: Return the initial state from which the problem is to be solved.
        goal_states(self) -> Generator[State]: Return the goal states of the problem.
        actions(self, state: State) -> list: Return a list of actions that can be executed in the given state.
        actions_to(self, state: State) -> list: Return a list of actions that can be executed in the given state.
        result(self, state: State, action: Action) -> State: Return the state that results from executing a given action in the given state.
        reason(self, state: State, action: Action) -> State: Return the state that can be taken the action to reach the given state.
        is_goal(self, state: State) -> bool: Check if the given state is a goal state.
        action_cost(self, s: State, action: Action) -> int|float: Return the cost of taking action from state to another state.
        heuristic(state: State) -> float: Returns the heuristic value of the given state.
        b_heuristic(state: State) -> float: Returns the backward heuristic value of the given state.
    """
    @abstractmethod
    def goal_states(self, state: State) -> list[State]:
        pass
    
    @abstractmethod
    def actions_to(self, state: State) -> list[Action]:
        pass
    
    @abstractmethod
    def reason(self, state: State, action: Action) -> State:
        pass
    
    @abstractmethod
    def re_heuristic(self, state: State) -> int|float:
        pass
    
class GameState(ABC):
    @abstractmethod
    def __init__(self, state: State, player: Enum) -> None:
        self.state = state
        self.player = Enum