from enum import auto
from sealgo.problem import State, Action, HeuristicSearchProblem

class MazeState(State):
    def __init__(self, position, goal):
        self.position = position
        self.goal = goal
    
    def __hash__(self):
        return hash(self.position)
    
    def __eq__(self, other):
        return isinstance(other, MazeState) and self.position == other.position
    
    def __lt__(self, other):
        return self.position < other.position

class MazeProblem(HeuristicSearchProblem):
    def __init__(self, initial, goal, maze):
        self.initial = MazeState(initial, goal)
        self.goal = MazeState(goal, goal)
        self.maze = maze

    def initial_state(self):
        return self.initial

    def actions(self, state):
        actions = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for d in directions:
            new_position = (state.position[0] + d[0], state.position[1] + d[1])
            if 0 <= new_position[0] < len(self.maze) and 0 <= new_position[1] < len(self.maze[0]) and self.maze[new_position[0]][new_position[1]] == 0:
                actions.append(Action(new_position))
        return actions

    def result(self, state, action):
        return MazeState(action.value, state.goal)

    def is_goal(self, state):
        return state == self.goal

    def action_cost(self, s, action):
        return 1

    def heuristic(self, state):
        return abs(state.position[0] - state.goal.position[0]) + abs(state.position[1] - state.goal.position[1])

class MazeAction(Action):
    MOVE = auto()
