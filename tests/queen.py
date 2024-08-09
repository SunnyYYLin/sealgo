import itertools
import random
from functools import lru_cache
from typing import Any
from enum import Enum, auto
from sealgo.problem import HeuristicSearchProblem, State, Action

MAX_CACHE = 100_000_000

class Piece(Enum):
    QUEEN = auto()
    EMPTY = auto()

class QState(tuple, State):
    def __str__(self) -> str:
        return '\n'.join([''.join(['Q' if self[i]==j else '.' for j in range(len(self))]) for i in range(len(self))])
    
    def __lt__(self, other: Any) -> bool:
        if isinstance(other, QState):
            return tuple.__lt__(self, other)
        return NotImplemented

class QAction(Action):
    def __init__(self, row: int, to_column: int) -> None:
        self.row = row
        self.to_column = to_column
        
    def __hash__(self) -> int:
        return hash((self.row, self.to_column))
    
    def __repr__(self) -> str:
        return f"R{self.row}:->C{self.to_column}"
    
    def __str__(self) -> str:
        return f"Queen at row {self.row} move onto {self.to_column}\n"
    
class EightQueens(HeuristicSearchProblem): # type: ignore
    def __init__(self, n: int = 8):
        self.scale = n
        
    def initial_state(self) -> QState:
        return QState(random.randint(0, self.scale-1) for _ in range(self.scale))
    
    def actions(self, state: QState) -> list[QAction]:
        return [QAction(i, j) for i, j in 
                itertools.product(range(self.scale), range(self.scale)) if j != state[i]]
    
    def result(self, state: QState, action: QAction) -> QState:
        return QState(state[:action.row] + (action.to_column,) + state[action.row+1:])
    
    def is_goal(self, state: QState) -> bool:
        return self.num_conflict_pairs(state) == 0
    
    def action_cost(self, s: State, action: Action) -> int:
        return 1
    
    def heuristic(self, state: QState) -> int:
        return self.num_conflict_pairs(state)
    
    @lru_cache(maxsize=MAX_CACHE)
    def num_conflict_pairs(self, state: QState) -> int:
        """
        Return the pairs of queens that conflict with each other.
        """
        n_conflict_pairs = 0
        for pos in enumerate(state):
            for other_pos in enumerate(state):
                if pos[0] < other_pos[0]:
                    if pos[1] == other_pos[1] or \
                        abs(pos[1] - other_pos[1]) == abs(pos[0] - other_pos[0]):
                        n_conflict_pairs += 1
        return n_conflict_pairs