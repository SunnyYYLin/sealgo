from sealgo.mcts import MCTS
from tests.queen import EightQueens
import numpy as np

def test_mcts(): 
    problem = EightQueens(8)
    mcts = MCTS(problem, time_limit=1000)
    
    solution = mcts.search()
    print("Solution:", solution)
    
if __name__ == "__main__":
    test_mcts()