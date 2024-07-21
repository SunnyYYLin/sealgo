# TODO
# import itertools
# from functools import lru_cache
# from typing import List, Tuple, Optional
# from sealgo.problem import HeuristicSearchProblem, GameState, Action

# MAX_CACHE = 100000
    
# class TicTacToe(HeuristicSearchProblem):
#     class TS(GameState):
#         def __init__(self, board:List[List[str]], to_move:str, cost:int=0):
#             '''board is an n*n list of string "X" or "O"'''
#             super().__init__(cost, to_move)
#             self.board = board
        
#         def __hash__(self):
#             '''convert list into tuple to hash it'''
#             return hash(self.__str__())
        
#         def __eq__(self, other):
#             return self.board == other.board
        
#         def __str__(self):
#             return '\n'.join(' '.join(self.board[i][j] if self.board[i][j] != '.' else '.' for j in range(len(self.board))) 
#                              for i in range(len(self.board))) \
#                                 #  + f'\n{self.to_move} to move'
        
#     def __init__(self):
#         """
#         Initialize the Tic-Tac-Toe problem.
#         """
#         self.scale = 3
#         self.players = ['X', 'O']
        
#     def initial_state(self) -> TS:
#         """
#         Return the initial state of the Tic-Tac-Toe problem.
#         """
#         return self.TS([['.' for _ in range(self.scale)] for _ in range(self.scale)], 'O')
    
#     def actions(self, state: TS) -> List[TA]:
#         """
#         Return the actions that can be executed in the given state.
#         """
#         actions = [(i, j) for i, j in itertools.product(range(self.scale), range(self.scale)) 
#                    if state.board[i][j] == '.']
#         # Considering symmetry for simplicity.
#         state_set = set()
#         reduced_actions = []
#         for action in actions:
#             # 每次计算结果时，都应从原始状态开始
#             new_state = self.result(state, action)
#             # 检查新状态及其所有对称形态是否都是新的
#             new_states = [new_state]
#             new_states.append(self.reflect(new_state))
#             for _ in range(3):
#                 new_state = self.rotate(new_state)
#                 new_states.append(new_state)
#                 new_states.append(self.reflect(new_state))
            
#             # 如果所有变形都是新的，则考虑这个动作
#             if not any(s in state_set for s in new_states):
#                 reduced_actions.append(action)
#                 state_set.update(new_states)  # 将所有新变形加入已知集合
                
#         return reduced_actions
    
#     def result(self, state:TS, action:TA) -> TS:
#         """
#         Return the state that results from executing a given action in the given state.
#         """
#         next_state = self.TS([row.copy() for row in state.board], 'X' if state.to_move == 'O' else 'O', state.cost + 1)
#         next_state.board[action[0]][action[1]] = state.to_move
#         return next_state
        
#     def is_goal(self, state) -> Optional[str]:
#         """
#         Check if the given state is a goal state. Return player who wins.
#         """
#         for player in self.players:
#             if self.count_patterns(state, player, self.scale) > 0:
#                 return player
#         if all(state.board[i][j] != '.' for i, j in itertools.product(range(self.scale), range(self.scale))):
#             return 'T'
#         return None
    
#     def heuristic(self, state:TS, player:str) -> int:
#         """
#         Return the heuristic value of the given state.
#         """
#         if self.is_goal(state) == player:
#             return 100
#         elif self.is_goal(state) == 'T':
#             return 0
#         else:
#             X2 = self.count_patterns(state, 'X', 2)
#             X1 = self.count_patterns(state, 'X', 1)
#             O2 = self.count_patterns(state, 'O', 2)
#             O1 = self.count_patterns(state, 'O', 1)
#             coef = 1 if player == 'X' else -1
#             return coef * (3*X2 + X1 - (3*O2 + O1))
    
#     def rotate(self, state) -> TS:
#         return self.TS([list(reversed(row)) for row in zip(*state.board)], state.to_move)
    
#     def reflect(self, state) -> TS:
#         return self.TS([list(reversed(row)) for row in state.board], state.to_move)
    
#     @lru_cache(maxsize=MAX_CACHE)
#     def count_patterns(self, state:State, player:int, count:int) -> int:
#         """
#         Count the number of rows, columns, and diagonals with exactly 'count' number of 'player' marks.
#         """
#         lines = []

#         # 添加所有行
#         lines.extend(state.board)

#         # 添加所有列
#         for col in range(self.scale):
#             lines.append(tuple(state.board[row][col] for row in range(self.scale)))

#         # 添加主对角线
#         lines.append(tuple(state.board[i][i] for i in range(self.scale)))

#         # 添加副对角线
#         lines.append(tuple(state.board[i][self.scale - 1 - i] for i in range(self.scale)))
        
#         return sum(1 for line in lines if line.count(player) == count and line.count('.') == self.scale - count)
    
# class RobotSearchProblem(UncertainSearchProblem):
#     class RS(State):
#         def __init__(self, position, cost=0):
#             super().__init__(cost)
#             self.position = position

#         def __hash__(self):
#             return hash(self.position)

#         def __eq__(self, other):
#             return self.position == other.position

#     class RA(Action):
#         def __init__(self, direction):
#             self.direction = direction
            
#         def __hash__(self):
#             return hash(self.direction)
        
#         def __eq__(self, other):
#             return self.direction == other.direction
            
#     def initial_state(self) -> State:
#         return self.RS((0, 0))

#     def actions(self, state: RS) -> List[RA]:
#         return [self.RA('north'), self.RA('south'), self.RA('east'), self.RA('west')]

#     def is_goal(self, state: RS) -> bool:
#         return state.position == (10, 10)

#     def result(self, state: RS, action: RA) -> List[Tuple[State, float]]:
#         # Simplified transition model with 80% success and 20% stay in place
#         new_position = self.calculate_new_position(state.position, action.direction)
#         state.cost += self.action_cost(state, action)
#         return [(self.RS(new_position, state.cost), 0.8), 
#                 (state, 0.2)]
        
#     def heuristic(self, state: RS) -> int:
#         return abs(state.position[0] - 10) + abs(state.position[1] - 10)

#     def calculate_new_position(self, position, direction):
#         x, y = position
#         if direction == 'north':
#             return (x, y+1)
#         elif direction == 'south':
#             return (x, y-1)
#         elif direction == 'east':
#             return (x+1, y)
#         elif direction == 'west':
#             return (x-1, y)

# if __name__ == '__main__':
#     problem = EightQueens()
#     print(problem.initial_state())
#     print(problem.actions(problem.initial_state()))
#     print(problem.result(problem.initial_state(), (0, 3)))
#     print(problem.is_goal(problem.initial_state()))
#     print(problem.heuristic(problem.initial_state()))