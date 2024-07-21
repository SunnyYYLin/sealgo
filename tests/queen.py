import itertools
import random
from functools import lru_cache
from typing import List, Tuple, Optional
from sealgo.problem import HeuristicSearchProblem, State, Action

MAX_CACHE = 100000

class EightQueens(HeuristicSearchProblem):
    class QS(State):
        '''
        The state of the eight queens problem including the board and the cost.
        '''
        def __init__(self, board:tuple, cost=0):
            self.board = board
            self.cost = cost
        
        def __str__(self):
            return '\n'.join(' '.join('Q' if j == self.board[i] else '.' for j in range(len(self.board))) 
                             for i in range(len(self.board)))
        
        def __hash__(self):
            return hash(self.board)
        
        def __eq__(self, other):
            return self.board == other.board
        
        def __lt__(self, other):
            return self.cost < other.cost
    
    class QA(Action, tuple[int, int]):
        '''
        (i, j): Move the i'th queen to the j'th column.
        '''
        pass
        
    def __init__(self, n: int = 8):
        """
        Initialize the eight queens problem with the scale.
        """
        self.scale = n
        
    def initial_state(self) -> QS:
        """
        Return the initial state of the eight queens problem. # (i, j) i: row, j: column to move to
        """
        return self.QS(tuple(random.randint(0, self.scale-1) for _ in range(0, self.scale)))
    
    def actions(self, state:QS) -> list[tuple[2]]:
        """
        Return the actions that can be executed in the given state.
        """
        return [(i, j) for i, j in itertools.product(range(self.scale), range(self.scale)) 
                if j != state.board[i]]
    
    def result(self, state: QS, action: QA) -> QS:
        """
        Return the state that results from executing a given action in the given state.
        """
        return self.QS(state.board[:action[0]] + (action[1],) + state.board[action[0]+1:], 
                       state.cost + self.action_cost(state, action))
    
    def is_goal(self, state: QS) -> bool:
        """
        Check if the given state is a goal state.
        """
        return self.num_conflict_pairs(state) == 0
    
    def heuristic(self, state: QS) -> int:
        """
        Return the heuristic value of the given state.
        """
        return self.num_conflict_pairs(state)
    
    @lru_cache(maxsize=MAX_CACHE)
    def num_conflict_pairs(self, state: QS) -> int:
        """
        Return the pairs of queens that conflict with each other.
        """
        n_conflict_pairs = 0
        for pos in enumerate(state.board):
            for other_pos in enumerate(state.board):
                if pos[0] < other_pos[0]:
                    if pos[1] == other_pos[1] or \
                        abs(pos[1] - other_pos[1]) == abs(pos[0] - other_pos[0]):
                        n_conflict_pairs += 1
        return n_conflict_pairs