import os
from typing import Optional

from .problem import Problem
from .team import Team

class Progcomp:
    def __init__(self) -> None:
        self._teams: dict[str, Team] = {}
        self._problems: dict[str, Problem] = {}
    
    def get_team(self, name: str) -> Optional[Team]:
        return self._teams.get(name)
    
    def add_team(self, name: str, password: str):
        self._teams[name] = Team(name, password)
    
    def update_problems(self):
        # Add any new problems, update existing ones
        path = os.path.join(os.getcwd(), "problems")
        p_names = os.listdir(path)
        for p_name in p_names:
            prob = self._problems.get(p_name)
            if not prob:
                self._problems[p_name] = Problem(p_name)
            else:
                prob.update()

    def get_problem(self, name):
        return self._problems.get(name)
    
    def get_pdf_loc(self):
        path = os.path.join(os.getcwd(), "pdf")
        return path

# p = Progcomp()
# p = print(p.get_problems())