import os
import json
import re
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
        print(f"\x1b[32mupdate({self})\x1b[0m")
        
        input_path = os.path.join(
            os.getcwd(),
            "problems",
            self.progcomp.name,
            self.name,
            "input",
        )

        output_path = os.path.join(
            os.getcwd(),
            "problems",
            self.progcomp.name,
            self.name,
            "output",
        )

        old = set((t.name, t.ext) for t in self.tests)

        def check(test_input_filename: str) -> Optional[tuple[str, str]]:
            if os.path.isfile(os.path.join(output_path, test_input_filename if not test_input_filename.endswith(".in") else test_input_filename.removesuffix(".in") + ".out")):
                match = re.search(r"^(.*)\.(.*)$", test_input_filename)
                return match.group(1), match.group(2)
            return None

        new = set(map(check, os.listdir(input_path)))
        new = set(s for s in new if s is not None)

        print("Old new", old, new)
        for test_name, test_ext in old - new:
            print(f"\x1b[32m{test_name}\x1b[0m")
            test = self.get_test(test_name)
            if test:
                db.session.delete(test)
                print("Removing Test", test)
        for test_name, test_ext in new - old:
            db.session.add(test := Test(problem_id=self.id, name=test_name, ext=test_ext))
            print("Adding Test", test)

        db.session.commit()
        
        # Check for Config
        config_path = os.path.join(
            os.getcwd(),
            "problems",
            self.progcomp.name,
            self.name,
            "config.json",
        )

        if (os.path.isfile(config_path)):
            with open(config_path) as f:
                config = json.load(f)

            # Ensure Config is up to date
            for test_name, test_ext in new:
                test_max = config[test_name]["max"]
                test_weight = config[test_name]["weight"]
                (test := self.get_test(test_name)).max_score = test_max
                test.weight = test_weight

        db.session.commit()
        db.session.flush()
        print(f"\x1b[36mTests: {self.tests}\x1b[0m")

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
    ext = sa.Column(sa.String, nullable=False)
    max_score = sa.Column(sa.Integer, nullable=True)
    weight = sa.Column(sa.Float, nullable=True)

    problem = relationship(Problem, back_populates="tests")
    submissions = relationship("Submission", back_populates="test")

    __table_args__ = (sa.UniqueConstraint("name", "problem_id", name="unq_tests_name"),)

    @property
    def input_path(self) -> str:
        return os.path.join(self.problem.path, "input", self.name + "." + self.ext)

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
            # We take earliest submission with highest score
            if (
                not current
                or (sub.score > current.score)
                or (sub.score == current.score and sub.timestamp < current.timestamp)
            ):
                team_scores[sub.team.name] = sub

        sub_list = list(team_scores.values())
        sub_list.sort(key=lambda s: (-s.score, s.timestamp))
        print(sub_list)
        return sub_list
