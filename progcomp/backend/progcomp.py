import os
from typing import Optional
from datetime import datetime

from .problem import Problem
from .team import Team
from .submission import Submission


class Progcomp:
    def __init__(self) -> None:
        self._teams: dict[str, Team] = {}
        self._problems: dict[str, Problem] = {}
        self._start_time = datetime.now()

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

    def get_timestamp(self):
        td = datetime.now() - self._start_time
        return str(td)[:-4].replace(":", "-")

    def make_submission(
        self, timestamp: str, team_name: str, p_name: str, test_name: str
    ):
        team = self._teams.get(team_name)
        problem = self._problems.get(p_name)
        if not team or not problem:
            return False
        team.add_submission(Submission(team, problem, timestamp, test_name))
        return True
