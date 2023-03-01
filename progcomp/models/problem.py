import os

from sqlalchemy import ForeignKey, ForeignKeyConstraint, func
from sqlalchemy.orm import relationship

from progcomp.models.utils import auto_str

from ..database import db


@auto_str
class Problem(db.Model):
    __tablename__ = "problems"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    progcomp_id = db.Column(db.Integer, ForeignKey("progcomps.id"))

    tests = relationship("Test", back_populates="problem")
    submissions = relationship("Submission", back_populates="problem")
    progcomp = relationship("Progcomp", back_populates="problems")

    def __init__(self):
        self.update()

    def update(self):
        path = os.path.join(os.getcwd(), "problems", self.name, "input")
        old = set(t.name for t in self.tests)
        new = set(os.listdir(path))

        for test_name in old - new:
            db.session.add(Test(problem_id=self.id, name=test_name))
        for test_name in new - old:
            test = db.query(Test).where(Test.name == test_name).first()
            db.session.remove(test)

    def get_test(self, name):
        return (
            db.session.query(Test)
            .where(Test.problem_id == self.id, Test.name == name)
            .first()
        )


@auto_str
class Test(db.Model):
    __tablename__ = "tests"

    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, ForeignKey(Problem.id))
    name = db.Column(db.String, unique=True)

    problem = relationship(Problem, back_populates="tests")
    submissions = relationship("Submission", back_populates="test")
