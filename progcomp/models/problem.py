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
    enabled = db.Column(db.Boolean, nullable=False, default=True)

    tests = relationship("Test", back_populates="problem", order_by="Test.name")
    submissions = relationship("Submission", back_populates="problem")
    progcomp = relationship("Progcomp", back_populates="problems")

    def update(self):
        path = os.path.join(os.getcwd(), "problems", self.name, "input")
        old = set(t.name for t in self.tests)
        new = set([x[:-4] for x in os.listdir(path)])

        print("Old new", old, new)
        for test_name in old - new:
            test = db.session.query(Test).where(Test.name == test_name).first()
            if test:
                db.session.delete(test)
        for test_name in new - old:
            db.session.add(test := Test(problem_id=self.id, name=test_name))
            print("Test", test)
        db.session.commit()

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
    name = db.Column(db.String, nullable=False)
    max_score = db.Column(db.Integer, nullable=True)

    problem = relationship(Problem, back_populates="tests")
    submissions = relationship("Submission", back_populates="test")
