import enum
import os
import subprocess

from sqlalchemy import ForeignKey, ForeignKeyConstraint, func
from sqlalchemy.orm import relationship

from progcomp.models.problem import Problem, Test
from progcomp.models.team import Team
from progcomp.models.utils import auto_str

from ..database import db


class Status(enum.Enum):
    UNKNOWN = 0
    SCORED = 1
    CORRECT = 2
    PARTIAL = 3
    WRONG = 4
    INVALID = 5


@auto_str
class Submission(db.Model):
    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, ForeignKey(Team.id))
    problem_id = db.Column(db.Integer, ForeignKey(Problem.id))
    test_id = db.Column(db.Integer, ForeignKey(Test.id), nullable=False)
    timestamp = db.Column(db.DateTime, default=func.current_timestamp())
    status = db.Column(db.Enum(Status), default=Status.UNKNOWN)
    score = db.Column(db.Integer)

    team = relationship(Team, back_populates="submissions")
    problem = relationship(Problem, back_populates="submissions")
    test = relationship(Test, back_populates="submissions")

    def __init__(self):
        self.mark()

    def mark(self):
        # Relative directories of the locations needed
        problem_dir = os.path.join("problems", self.problem.name)
        mark_file = os.path.join(problem_dir, "mark.py")
        submission_file = os.path.join(
            "submissions",
            self.team.name,
            self.problem.name,
            self.test.name,
            self.timestamp,
            "output.txt",
        )

        # Needs to be in a subprocess so we can add and remove on the fly
        ps = subprocess.run(
            [
                "python",
                mark_file,
                problem_dir,
                self.test_name + ".txt",
                submission_file,
            ],
            capture_output=True,
            text=True,
        )

        print(f"Errors in marking {self.problem.name}: {ps.stderr}")

        line = ps.stdout.strip("\n")

        nums = [int(n) for n in line.split()]

        if len(nums) == 2:
            self.score, self.max_score = nums
            if self.score == 0:
                self.status = Status.WRONG
            elif self.score == self.max_score:
                self.status = Status.CORRECT
            else:
                self.status = Status.PARTIAL
        elif len(nums) == 1:
            self.score = nums
            self.status = Status.SCORED
        else:
            self.status = Status.INVALID
