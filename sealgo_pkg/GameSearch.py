from Problem import *
from SearchAlgo import Search
from abc import abstractmethod
import networkx as nx
import matplotlib.pyplot as plt
import os
import matplotlib.image as mpimg
from networkx.drawing.nx_pydot import to_pydot
        
class Minimax(Search):
    """
    UNFINISHED
    """
    def __init__(self, problem: HeuristicSearchProblem, init: GameState, depth: int = 3):
        super().__init__(problem)
        self.state = init
        self.depth = depth
        
    def search(self) -> GameAction:
        def max_value(state, alpha, beta, depth) -> int:
            if depth == 0 or self.problem.is_goal(state):
                return self.problem.heuristic(state, self.state.to_move)
            v = float('-inf')
            for action in self.problem.actions(state):
                new_state = self.problem.result(state, action)
                print(f'{new_state}\nAlpha: {alpha}, Beta: {beta}')
                v = max(v, min_value(new_state, alpha, beta, depth - 1))
                if v >= beta:
                    print(f'Pruning beta: {v}')
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(state, alpha, beta, depth) -> int:
            if depth == 0 or self.problem.is_goal(state):
                return self.problem.heuristic(state, self.state.to_move)
            v = float('inf')
            for action in self.problem.actions(state):
                new_state = self.problem.result(state, action)
                print(f'{new_state}\nAlpha: {alpha}, Beta: {beta}')
                v = min(v, max_value(new_state, alpha, beta, depth - 1))
                if v <= alpha:
                    print(f'Pruning alpha: {v}')
                    return v
                beta = min(beta, v)
            return v

        best_score = float('-inf')
        best_action = None
        alpha = float('-inf')
        beta = float('inf')
        for action in self.problem.actions(self.state):
            new_state = self.problem.result(self.state, action)
            print(f'{new_state}\nAlpha: {alpha}, Beta: {beta}')
            score = min_value(new_state, alpha, beta, self.depth - 1)
            if score > best_score:
                best_score = score
                best_action = action
                alpha = max(alpha, score)
        return best_action
    
    def game_tree(self) -> nx.DiGraph:
        def max_value(state, alpha, beta, depth) -> int:
            if depth == 0 or self.problem.is_goal(state):
                return self.problem.heuristic(state, self.state.to_move)
            v = float('-inf')
            for action in self.problem.actions(state):
                new_state = self.problem.result(state, action)
                G.add_node(str(new_state))
                G.add_edge(str(state), str(new_state), label=action)
                v = max(v, min_value(new_state, alpha, beta, depth - 1))
                print(f'{new_state}\nAlpha: {alpha}, Beta: {beta}')
                
                if v >= beta:
                    print(f'Pruning beta: {v}')
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(state, alpha, beta, depth) -> int:
            if depth == 0 or self.problem.is_goal(state):
                return self.problem.heuristic(state, self.state.to_move)
            v = float('inf')
            for action in self.problem.actions(state):
                new_state = self.problem.result(state, action)
                G.add_node(str(new_state))
                G.add_edge(str(state), str(new_state), label=action)
                v = min(v, max_value(new_state, alpha, beta, depth - 1))
                
                print(f'{new_state}\nAlpha: {alpha}, Beta: {beta}')
                if v <= alpha:
                    print(f'Pruning alpha: {v}')
                    return v
                beta = min(beta, v)
            return v

        best_score = float('-inf')
        best_action = None
        alpha = float('-inf')
        beta = float('inf')
        G = nx.DiGraph()
        G.add_node(str(self.state))
        for action in self.problem.actions(self.state):
            new_state = self.problem.result(self.state, action)
            G.add_node(str(new_state))
            G.add_edge(str(self.state), str(new_state), label=action)
            print(f'{new_state}\nAlpha: {alpha}, Beta: {beta}')
            score = min_value(new_state, alpha, beta, self.depth - 1)
            if score > best_score:
                best_score = score
                alpha = max(alpha, score)
        return G
        
def draw_hierarchy(G):
    # 将networkx图转换为pydot图
    P = to_pydot(G)
    # 使用Graphviz的'dot'引擎来布局图
    P.write_png('temp_tree.png', prog='dot')

    # 使用matplotlib展示图像
    img = mpimg.imread('temp_tree.png')
    plt.figure(figsize=(10, 10))
    plt.imshow(img)
    plt.axis('off')
    plt.show()
    
if __name__ == '__main__':
    from ExampleProblem import TicTacToe
    problem = TicTacToe()
    init = problem.initial_state()
    # init.board[0][0] = 'X'
    print(init)
    minimax = Minimax(problem, init, depth=3)
    print(str(init))
    gt = minimax.game_tree()
    
    # draw gt
    pos = nx.spring_layout(gt)
    # print gt
    gt_str = nx.draw_networkx_labels(gt, pos)
    
    # draw gt
    nx.draw(gt, pos, with_labels=True)
    edge_labels = nx.get_edge_attributes(gt, 'label')
    nx.draw_networkx_edge_labels(gt, pos, edge_labels=edge_labels)
    plt.show()