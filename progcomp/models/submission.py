import enum
import logging
import os
import subprocess

import sqlalchemy as sa
from sqlalchemy import ForeignKey, ForeignKeyConstraint, func
from sqlalchemy.orm import relationship

from progcomp.models.problem import Problem, Test

# from progcomp.models.team import Team
from progcomp.models.utils import Status, auto_str

from ..database import Base, db


@auto_str
class Submission(Base):
    __tablename__ = "submissions"

    id = sa.Column(sa.Integer, primary_key=True)
    team_id = sa.Column(sa.Integer, ForeignKey("teams.id"))
    problem_id = sa.Column(sa.Integer, ForeignKey(Problem.id), nullable=False)
    test_id = sa.Column(sa.Integer, ForeignKey(Test.id), nullable=False)
    timestamp = sa.Column(sa.DateTime, default=func.current_timestamp())
    status = sa.Column(sa.Enum(Status), default=Status.UNKNOWN)
    directory = sa.Column(sa.String, nullable=False)
    score = sa.Column(sa.Integer)

    team = relationship("Team", back_populates="submissions")
    problem = relationship(Problem, back_populates="submissions")
    test = relationship(Test, back_populates="submissions")

    @property
    def time_str(self) -> str:
        return self.timestamp.strftime("%H:%M:%S")

    @property
    def status_str(self) -> str:
        return str(self.status)[len("Status") + 1 :]

    def mark(self) -> None:
        # Relative directories of the locations needed
        problem_dir = self.problem.path
        mark_file = os.path.join(problem_dir, "mark.py")
        submission_file = os.path.join(
            self.directory,
            "output.txt",
        )

        # Needs to be in a subprocess so we can add and remove on the fly
        ps = subprocess.run(
            [
                "python",
                mark_file,
                problem_dir,
                self.test.name
                + "."
                + ("out" if self.test.ext == "in" else self.test.ext),
                submission_file,
            ],
            capture_output=True,
            text=True,
        )

        logging.warning(f"Errors in marking {self.problem.name}: {ps.stderr}")

        line = ps.stdout.strip("\n")

        nums = [int(n) for n in line.split()]

        if len(nums) > 0:
            self.score = nums[0]

            # Optimisation Problems
            if not self.test.max_score:
                self.status = Status.SCORED

            # Max-Score Problems
            elif self.score == 0:
                self.status = Status.WRONG
            elif self.score == self.test.max_score:
                self.status = Status.CORRECT
            else:
                self.status = Status.PARTIAL

        else:
            self.status = Status.INVALID

        logging.info(
            f"New Submission for {self.problem.name}: {self.test.name} by {self.team.name} [{self.status}] {self.score}/{self.test.max_score or ''}"
        )
