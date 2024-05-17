from abc import ABC, abstractmethod
import itertools
import random

class State(ABC):
    @abstractmethod
    def __hash__(self):
        pass
    
    @abstractmethod
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
    
class Action(ABC):
    @abstractmethod
    def __hash__(self):
        pass
    
    @abstractmethod
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

class SearchProblem(ABC):
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

    @abstractmethod
    def action_cost(self, s: State, action: Action) -> float:
        """Return the cost of taking action from state to another state."""
        return 1
    
class HeuristicSearchProblem(SearchProblem):
    @abstractmethod
    def heuristic(self, state: State) -> float:
        """Return the heuristic value of the given state."""
        pass
    
class EightQueens(HeuristicSearchProblem):
    def __init__(self, n: int = 8):
        """
        Initialize the eight queens problem with the scale.
        """
        self.scale = n
        
    def initial_state(self):
        """
        Return the initial state of the eight queens problem. # (i, j) i: row, j: column to move to
        """
        return tuple(random.randint(0, self.scale-1) for _ in range(0, self.scale))
    
    def actions(self, state):
        """
        Return the actions that can be executed in the given state.
        """
        return [(i, j) for i, j in itertools.product(range(self.scale), range(self.scale)) if j != state[i]]
    
    def result(self, state, action):
        """
        Return the state that results from executing a given action in the given state.
        """
        return state[:action[0]] + (action[1],) + state[action[0]+1:]
    
    def is_goal(self, state):
        """
        Check if the given state is a goal state.
        """
        return self.num_conflict_pairs(state) == 0
    
    def heuristic(self, state):
        """
        Return the heuristic value of the given state.
        """
        return self.num_conflict_pairs(state)
    
    def num_conflict_pairs(self, state):
        """
        Return the pairs of queens that conflict with each other.
        """
        n_conflict_pairs = 0
        for pos in enumerate(state):
            for other_pos in enumerate(state):
                if pos[0] < other_pos[0]:
                    if pos[1] == other_pos[1] or abs(pos[1] - other_pos[1]) == abs(pos[0] - other_pos[0]):
                        n_conflict_pairs += 1
        return n_conflict_pairs
    
class TicTacToe(HeuristicSearchProblem):
    stone = ['X', 'O']
    player = {'X': 0, 'O': 1}
    
    class TState(State):
        
        def __init__(self, board:list, latest_player_num:int):
            '''board is an n*n list of string "X" or "O", palyer_n: {0:"X", 1:"O"}'''
            self.board = board
            self.player_n = latest_player_num
        
        def __hash__(self):
            '''convert list into tuple to hash it'''
            return hash((tuple(self.board), self.player))
        
        def __eq__(self, other):
            return self.board == other.board and self.player == other.player
        
    class TAction(Action, tuple[int, int]):
        '''drop at (TAction[0], TAction[1])'''
        pass
        
    def __init__(self):
        """
        Initialize the Tic-Tac-Toe problem.
        """
        self.scale = 3
        self.players = ['X', 'O']
        
    def initial_state(self) -> TState:
        """
        Return the initial state of the Tic-Tac-Toe problem.
        """
        return self.TState([['' for _ in range(self.scale)] for _ in range(self.scale)], 1) # player for latest move
    
    def actions(self, state: TState):
        """
        Return the actions that can be executed in the given state.
        """
        actions = [(i, j) for i, j in itertools.product(range(self.scale), range(self.scale)) if state.board[i][j] == '']
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
    
    def result(self, state:TState, action:TAction):
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
    
    def count_patterns(self, state:State, player:int, count:int) -> int:
        """
        Count the number of rows, columns, and diagonals with exactly 'count' number of 'player' marks.
        """
        lines = []
        
        # Rows and columns
        
        
        # Diagonals
        
        
        # Count patterns
        return sum(1 for line in lines if line.count(player) == count and line.count(' ') == self.scale - count)