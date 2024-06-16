from Problem import HeuristicSearchProblem, UncertainSearchProblem, State, Action
import itertools
import random
from functools import lru_cache
from typing import List, Tuple, Optional

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
    
class TicTacToe(HeuristicSearchProblem):
    stone = ['X', 'O']
    player = {'X': 0, 'O': 1}
    
    class TS(State):
        def __init__(self, board:list, latest_player_num:int, cost:int=0):
            '''board is an n*n list of string "X" or "O", palyer_n: {0:"X", 1:"O"}'''
            self.board = board
            self.player_n = latest_player_num
            self.cost = cost
        
        def __hash__(self):
            '''convert list into tuple to hash it'''
            return hash((tuple(self.board), self.player))
        
        def __eq__(self, other):
            return self.board == other.board and self.player == other.player
        
    class TA(Action, tuple[int, int]):
        '''drop at (TAction[0], TAction[1])'''
        pass
        
    def __init__(self):
        """
        Initialize the Tic-Tac-Toe problem.
        """
        self.scale = 3
        self.players = ['X', 'O']
        
    def initial_state(self) -> TS:
        """
        Return the initial state of the Tic-Tac-Toe problem.
        """
        return self.TState([['' for _ in range(self.scale)] for _ in range(self.scale)], 1) # player for latest move
    
    def actions(self, state: TS):
        """
        Return the actions that can be executed in the given state.
        """
        actions = [(i, j) for i, j in itertools.product(range(self.scale), range(self.scale)) 
                   if state.board[i][j] == '']
        # Considering symmetry for simplicity.
        state_set = set()
        reduced_actions = set()
        for action in actions:
            is_new = False
            state = self.result(state, action)
            for _ in range(4):
                state = self.rotate(state)
                if state[0] not in state_set:
                    state_set.add(state)
                    is_new = True
                r_state = self.reflect(state)
                if r_state not in state_set:
                    state_set.add(state)
                    is_new = True
            if is_new:
                reduced_actions.add(action)
        return list(reduced_actions)
    
    def result(self, state:TS, action:TA):
        """
        Return the state that results from executing a given action in the given state.
        """
        state.player_n = 1 - state.player_n
        state.board[action[0], action[1]] = stone[player_n]
        
    def is_goal(self, state):
        """
        Check if the given state is a goal state.
        """
        return self.count_patterns(state, self.players[0], self.scale) > 0 \
                or self.count_patterns(state, self.players[1], self.scale) > 0 \
                or state.count(' ') == 0
    
    def heuristic(self, state):
        """
        Return the heuristic value of the given state.
        """
        if self.is_goal(state):
            for player in self.players:
                if self.count_patterns(state, player, 3) > 0:
                    return 1 if player == 'X' else -1
            return 0
        else:
            X2 = self.count_patterns(state, 'X', 2)
            X1 = self.count_patterns(state, 'X', 1)
            O2 = self.count_patterns(state, 'O', 2)
            O1 = self.count_patterns(state, 'O', 1)
            return 3*X2 + X1 - (3*O2 + O1)
    
    def rotate(self, state):
        return (tuple(tuple(state[0][j][-i] for j in range(self.scale)) for i in range(self.scale)), state[1])
    
    def reflect(self, state):
        return (tuple(tuple(state[0][i][j] for j in range(self.scale-1, -1, -1)) for i in range(self.scale)), state[1])
    
    @lru_cache(maxsize=MAX_CACHE)
    def count_patterns(self, state:State, player:int, count:int) -> int:
        """
        Count the number of rows, columns, and diagonals with exactly 'count' number of 'player' marks.
        """
        lines = []
        
        # Rows and columns
        
        
        # Diagonals
        
        
        # Count patterns
        return sum(1 for line in lines if line.count(player) == count and line.count(' ') == self.scale - count)
    
class RobotSearchProblem(UncertainSearchProblem):
    class RS(State):
        def __init__(self, position, cost=0):
            super().__init__(cost)
            self.position = position

        def __hash__(self):
            return hash(self.position)

        def __eq__(self, other):
            return self.position == other.position

    class RA(Action):
        def __init__(self, direction):
            self.direction = direction
            
        def __hash__(self):
            return hash(self.direction)
        
        def __eq__(self, other):
            return self.direction == other.direction
            
    def initial_state(self) -> State:
        return self.RS((0, 0))

    def actions(self, state: RS) -> List[RA]:
        return [self.RA('north'), self.RA('south'), self.RA('east'), self.RA('west')]

    def is_goal(self, state: RS) -> bool:
        return state.position == (10, 10)

    def result(self, state: RS, action: RA) -> List[Tuple[State, float]]:
        # Simplified transition model with 80% success and 20% stay in place
        new_position = self.calculate_new_position(state.position, action.direction)
        state.cost += self.action_cost(state, action)
        return [(self.RS(new_position, state.cost), 0.8), 
                (state, 0.2)]
        
    def heuristic(self, state: RS) -> int:
        return abs(state.position[0] - 10) + abs(state.position[1] - 10)

    def calculate_new_position(self, position, direction):
        x, y = position
        if direction == 'north':
            return (x, y+1)
        elif direction == 'south':
            return (x, y-1)
        elif direction == 'east':
            return (x+1, y)
        elif direction == 'west':
            return (x-1, y)

if __name__ == '__main__':
    problem = EightQueens()
    print(problem.initial_state())
    print(problem.actions(problem.initial_state()))
    print(problem.result(problem.initial_state(), (0, 3)))
    print(problem.is_goal(problem.initial_state()))
    print(problem.heuristic(problem.initial_state()))