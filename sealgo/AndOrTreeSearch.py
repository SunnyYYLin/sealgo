from abc import abstractmethod
from sealgo.sealgo.Search import Search
from Problem import UncertainSearchProblem, State, Action
import diagrams as diag
from typing import Optional, List
    
class AndOrTreeSearch:
    def __init__(self, problem: UncertainSearchProblem):
        self.problem = problem
        self.reached = {}

    def search(self) -> Optional[State]:
        initial_state = self.problem.initial_state()
        return self.or_search(initial_state)

    def or_search(self, state: State) -> Optional[State]:
        if self.problem.is_goal(state):
            return state
        if state in self.reached:
            return self.reached[state]
        self.reached[state] = self.problem.heuristic(state)
        for action in self.problem.actions(state):
            results = self.problem.result(state, action)
            for result_state, probability in results:
                if probability > 0:
                    plan = self.and_search(result_state)
                    if plan is not None:
                        return plan
        return None

    def and_search(self, state: State) -> Optional[State]:
        if self.problem.is_goal(state):
            return state
        if state in self.reached:
            return None
        self.reached[state] = self.problem.heuristic(state)
        plan_all = []
        for action in self.problem.actions(state):
            results = self.problem.result(state, action)
            plan_sub = []
            for result_state, probability in results:
                if probability > 0:
                    plan = self.or_search(result_state)
                    if plan is None:
                        break
                    plan_sub.append(plan)
            if len(plan_sub) == len(results):
                plan_all.append(plan_sub)
        return plan_all[0] if plan_all else None
    
if __name__ == '__main__':
    from ExampleProblem import RobotSearchProblem
    problem = RobotSearchProblem()
    search = AndOrTreeSearch(problem)
    print(search.search())