from sealgo_pkg.LocalSearch import StochasticHillClimbing
from sealgo_pkg.Problem import EightQueens

problem = EightQueens(8)
for _ in range(1000):
    search = StochasticHillClimbing(problem)
    if search.search():
        print(search.state)