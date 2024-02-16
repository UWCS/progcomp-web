import os
import typing
from typing import Optional

import sqlalchemy as sa
from sqlalchemy import ForeignKey, ForeignKeyConstraint, UniqueConstraint, func
from sqlalchemy.orm import relationship

from progcomp.models.utils import Status, Visibility, auto_str

if typing.TYPE_CHECKING:
    from progcomp.models.submission import *

from ..database import Base, db


@auto_str
class Problem(Base):
    __tablename__ = "problems"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    progcomp_id = sa.Column(sa.Integer, ForeignKey("progcomps.id"))
    visibility = sa.Column(
        sa.Enum(Visibility),
        nullable=False,
        default=Visibility.OPEN,
        server_default="OPEN",
    )
    __table_args__ = (
        sa.UniqueConstraint("name", "progcomp_id", name="unq_problems_name"),
    )

    tests = relationship("Test", back_populates="problem", order_by="Test.name")
    submissions = relationship("Submission", back_populates="problem")
    progcomp = relationship("Progcomp", back_populates="problems")

    @property
    def path(self) -> str:
        return os.path.join(os.getcwd(), "problems", self.progcomp.name, self.name)

    @property
    def visible(self) -> Visibility:
        return min(self.visibility, self.progcomp.visible)

    @property
    def open(self) -> bool:
        return self.visible == Visibility.OPEN

    def update(self) -> None:
        path = os.path.join(
            os.getcwd(),
            "problems",
            self.progcomp.name,
            self.name,
            "input",
        )
        old = set(t.name for t in self.tests)
        print("path:", os.listdir(path))
        new = set([x.rstrip(".txt") for x in os.listdir(path) if x.endswith(".txt")])

        print("Old new", old, new)
        for test_name in old - new:
            test = self.get_test(test_name)
            if test:
                db.session.delete(test)
                print("Removing Test", test)
        for test_name in new - old:
            db.session.add(test := Test(problem_id=self.id, name=test_name))
            print("Adding Test", test)
        db.session.commit()
        db.session.flush()

    def get_test(self, name: str) -> Optional["Test"]:
        return (
            db.session.query(Test)
            .where(Test.problem_id == self.id)
            .where(Test.name == name)
            .first()
        )


@auto_str
class Test(Base):
    __tablename__ = "tests"

    id = sa.Column(sa.Integer, primary_key=True)
    problem_id = sa.Column(sa.Integer, ForeignKey(Problem.id))
    name = sa.Column(sa.String, nullable=False)
    max_score = sa.Column(sa.Integer, nullable=True)

    problem = relationship(Problem, back_populates="tests")
    submissions = relationship("Submission", back_populates="test")

    __table_args__ = (sa.UniqueConstraint("name", "problem_id", name="unq_tests_name"),)

    @property
    def input_path(self) -> str:
        return os.path.join(self.problem.path, "input", self.name + ".txt")

    @property
    def ranked_submissions(self) -> list["Submission"]:
        from progcomp.models import Submission

        submissions = (
            db.session.query(Submission).where(Submission.test_id == self.id).all()
        )

        team_scores: dict[str, "Submission"] = {}

        for sub in submissions:
            if sub.status not in [Status.CORRECT, Status.PARTIAL, Status.SCORED]:
                continue
            current = team_scores.get(sub.team.name)
            if (
                not current
                or (sub.score > current.score)
                or (sub.score == current.score and sub.timestamp > current.timestamp)
            ):
                team_scores[sub.team.name] = sub

        sub_list = list(team_scores.values())
        sub_list.sort(key=lambda s: (-s.score, s.timestamp))
        print(sub_list)
        return sub_list
