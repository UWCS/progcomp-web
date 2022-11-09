import os
import subprocess
from .problem import Problem
from .team import Team

class Submission:
    def __init__(self, team: Team, problem: Problem, timestamp: str, test_name: str) -> None:
        self.team: Team = team
        self.problem: Problem = problem
        self.timestamp: str = timestamp
        self.test_name : str = test_name
        self.status : str = "UNKNOWN"
        self.score : int = 0
        self.max_score : int = -1  # -1 means no max score

        # Run in separate thread?
        self.mark()
    
    def mark(self):
        # Relative directories of the locations needed
        problem_dir = os.path.join("problems", self.problem.name)
        mark_file = os.path.join(problem_dir, "mark.py")
        submission_file = os.path.join(
            "submissions", 
            self.team.name, 
            self.problem.name, 
            self.test_name, 
            self.timestamp,
            "output.txt"
        )

        # Needs to be in a subprocess so we can add and remove on the fly
        ps = subprocess.run(
            ["python", mark_file, problem_dir, self.test_name + ".txt", submission_file], 
            capture_output=True, 
            text=True
        )

        print(f"Err: {ps.stderr}")

        line = ps.stdout.strip("\n")
        print(line)
        nums = [int(n) for n in line.split()]

        if len(nums) == 2:
            self.score, self.max_score = nums
            if self.score == 0:
                self.status = "WRONG"
            elif self.score == self.max_score:
                self.status = "CORRECT"
            else:
                self.status = "PARTIAL"
        elif len(nums) == 1:
            self.score = nums
            self.status = "SCORED"
        else:
            self.status = "INVALID"
