import os
import typing
from typing import Optional

from sqlalchemy import ForeignKey, ForeignKeyConstraint, func
from sqlalchemy.orm import relationship

from progcomp.models.utils import Status, Visibility, auto_str

if typing.TYPE_CHECKING:
    from progcomp.models.submission import *

from ..database import Base, db


@auto_str
class Problem(Base):
    __tablename__ = "problems"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    progcomp_id = db.Column(db.Integer, ForeignKey("progcomps.id"))
    visibility = db.Column(
        db.Enum(Visibility),
        nullable=False,
        default=Visibility.OPEN,
        server_default="OPEN",
    )
    db.UniqueConstraint("Problem.name", "Problem.progcomp_id", name="unq_problem_name")

    tests = relationship("Test", back_populates="problem", order_by="Test.name")
    submissions = relationship("Submission", back_populates="problem")
    progcomp = relationship("Progcomp", back_populates="problems")

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
        new = set([x[:-4] for x in os.listdir(path)])

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

    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, ForeignKey(Problem.id))
    name = db.Column(db.String, nullable=False)
    max_score = db.Column(db.Integer, nullable=True)

    problem = relationship(Problem, back_populates="tests")
    submissions = relationship("Submission", back_populates="test")

    db.UniqueConstraint("Test.name", "Test.problem_id", "unq_test_name")

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
