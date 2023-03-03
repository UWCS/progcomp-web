import enum
import logging
import os
import subprocess

from sqlalchemy import ForeignKey, ForeignKeyConstraint, func
from sqlalchemy.orm import relationship

from progcomp.models.problem import Problem, Test

# from progcomp.models.team import Team
from progcomp.models.utils import Status, auto_str

from ..database import Base, db


@auto_str
class Submission(Base):
    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, ForeignKey("teams.id"))
    problem_id = db.Column(db.Integer, ForeignKey(Problem.id))
    test_id = db.Column(db.Integer, ForeignKey(Test.id), nullable=False)
    timestamp = db.Column(db.DateTime, default=func.current_timestamp())
    status = db.Column(db.Enum(Status), default=Status.UNKNOWN)
    directory = db.Column(db.String, nullable=False)
    score = db.Column(db.Integer)

    team = relationship("Team", back_populates="submissions")
    problem = relationship(Problem, back_populates="submissions")
    test = relationship(Test, back_populates="submissions")

    @property
    def time_str(self) -> str:
        return self.problem.progcomp.get_timestamp_str(self.timestamp)

    @property
    def status_str(self) -> str:
        return str(self.status)[len("Status") + 1 :]

    def mark(self) -> None:
        # Relative directories of the locations needed
        problem_dir = os.path.join("problems", self.problem.name)
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
                self.test.name + ".txt",
                submission_file,
            ],
            capture_output=True,
            text=True,
        )

        logging.warning(f"Errors in marking {self.problem.name}: {ps.stderr}")

        line = ps.stdout.strip("\n")

        nums = [int(n) for n in line.split()]

        if len(nums) == 2:
            self.score, max_score = nums
            if self.test.max_score is None:
                self.test.max_score = max_score
            if self.score == 0:
                self.status = Status.WRONG
            elif self.score == self.test.max_score:
                self.status = Status.CORRECT
            else:
                self.status = Status.PARTIAL
        elif len(nums) == 1:
            (self.score,) = nums
            self.status = Status.SCORED
        else:
            self.status = Status.INVALID

        logging.info(
            f"New Submission for {self.problem.name}: {self.test.name} by {self.team.name} [{self.status}] {self.score}/{self.test.max_score or ''}"
        )
