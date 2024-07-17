# from sealgo.sealgo_pkg.Search import Search
# from Problem import SearchProblem, HeuristicSearchProblem, State, Action
# from abc import abstractmethod
# from queue import PriorityQueue, Queue, LifoQueue

# class BestFirstSearch(Search):
#     def __init__(self, problem:SearchProblem, eval_f = lambda x: x.cost, qtype = PriorityQueue):
#         '''
#         '''
#         super().__init__(problem)
#         self.reached = {}
#         self.qtype = qtype
#         self.frontier = self.qtype()
#         self.eval_f = eval_f
#         init = problem.initial_state()
#         if qtype == Queue or qtype == LifoQueue:
#             self.frontier.put(init)
#         elif qtype == PriorityQueue:
#             self.frontier.put((self.eval_f(init), init))
#         else:
#             raise ValueError('Invalid queue type.')
        
#     def search(self, only_one = True):
#         if not only_one:
#             goals = []
#         while not self.frontier.empty():
#             if self.qtype == PriorityQueue:
#                 state = self.frontier.get()[1]
#             else:
#                 state = self.frontier.get()
#             if self.problem.is_goal(state):
#                 if only_one:
#                     return state
#                 goals.append(state)
#                 # print(f'Goal:\n{state}\n{state.cost}\n')
#             self.reached[state] = state.cost
#             print(f'Reached:\n{state}\n{state.cost}\n{self.eval_f(state)}\n')
#             for action in self.problem.actions(state):
#                 next_state = self.problem.result(state, action)
#                 if next_state not in self.reached or next_state.cost < self.reached[next_state]:
#                     if self.qtype == PriorityQueue:
#                         self.frontier.put((self.eval_f(next_state), next_state))
#                     else:
#                         self.frontier.put(next_state)
#         return goals

# class BFS(BestFirstSearch):
#     def __init__(self, problem:SearchProblem):
#         super().__init__(problem, eval_f = lambda x: x.cost, qtype = Queue)
    
# class DFS(BestFirstSearch):
#     def __init__(self, problem:SearchProblem, max_depth = 100):
#         def f(x):
#             return -x.cost if x.cost < max_depth else 100
#         super().__init__(problem, eval_f = f, qtype = LifoQueue)
        
# class IDS(Search):
#     def __init__(self, problem:SearchProblem, max_depth = 100):
#         super().__init__(problem)
#         self.max_depth = max_depth
        
#     def search(self, only_one=True):
#         for depth in range(1, self.max_depth):
#             dfs = DFS(self.problem, depth)
#             result = dfs.search(only_one)
#             if result:
#                 return result
        
# class Dijkstra(BestFirstSearch):
#     def __init__(self, problem:SearchProblem):
#         super().__init__(problem, eval_f = lambda x: x.cost, qtype = PriorityQueue)
        
# class GBFS(BestFirstSearch):
#     def __init__(self, problem:HeuristicSearchProblem):
#         super().__init__(problem, eval_f = lambda x: problem.heuristic(x), qtype = PriorityQueue)
        
# class AStar(BestFirstSearch):
#     def __init__(self, problem:HeuristicSearchProblem, weight:float=1):
#         super().__init__(problem, eval_f = lambda x: x.cost+weight*problem.heuristic(x), qtype = PriorityQueue)
        
# class BiBFS(Search):
#     def __init__(self, problem:SearchProblem, goal_state, eval_f1=lambda x:x.cost, eval_f2=lambda x:x.cost):
#         super().__init__(problem)
#         self.reached1 = {}
#         self.reached2 = {}
#         self.eval_f1 = eval_f1
#         self.eval_f2 = eval_f2
#         self.frontier1 = PriorityQueue()
#         self.frontier2 = PriorityQueue()
#         self.frontier1.put((self.eval_f1(problem.initial_state()), problem.initial_state()))
#         self.frontier2.put((self.eval_f2(goal_state), goal_state))
    
#     def search(self):
#         while not self.frontier1.empty() and not self.frontier2.empty():
#             state1 = self.frontier1.get()[1]
#             state2 = self.frontier2.get()[1]
#             if state1 in self.reached2:
#                 return state1
#             if state2 in self.reached1:
#                 return state2
#             self.reached1[state1] = state1.cost
#             self.reached2[state2] = state2.cost
#             for action in self.problem.actions(state1):
#                 next_state = self.problem.result(state1, action)
#                 if next_state not in self.reached1 or next_state.cost < self.reached1[next_state]:
#                     self.frontier1.put((self.eval_f1(next_state), next_state))
#             for action in self.problem.actions(state2):
#                 last_state = self.problem.result(state2, action)
#                 if last_state not in self.reached2 or last_state.cost < self.reached2[last_state]:
#                     self.frontier2.put((self.eval_f2(last_state), last_state))
#         return None
    

    
# if __name__ == '__main__':
#     from ExampleProblem import EightQueens
#     problem = EightQueens(8)
#     algo = DFS(problem)
#     print(algo.search())