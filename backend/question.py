from enum import IntEnum
from datetime import datetime
from random import shuffle


class AnswerType(IntEnum):
    CORRECT = 1
    INCORRECT = 2
    TIMEOUT = 3


class Question:
    def __init__(self, difficulty, text, correct, wrong):
        """
        Represents a Quiz question

        :param difficulty:
        :param text: the question's text
        :param correct: the correct answer
        :param wrong: list containing all of the wrong answers
        """
        self.difficulty: int = difficulty
        self.text: str = text
        self.correct: str = correct
        self.wrong: list[str] = wrong
    
    def get_options(self) -> tuple[list[str], int]:
        options = [self.correct] + self.wrong.copy()
        shuffle(options)
        return options, options.index(self.correct)

    def __repr__(self):
        return f'Question({self.difficulty}, "{self.text}", {self.correct})'


# Feel free to ignore the implementation details of QuestionAttempt
class QuestionAttempt:
    def __init__(self, start, deadline, submitted_at=None):
        self.start: datetime = start
        self.deadline: datetime = deadline
        self.submitted_at: datetime = submitted_at

    @property
    def end_timestamp(self):
        return self.deadline.timestamp() * 1000

    @property
    def has_timed_out(self):
        return datetime.now() > self.deadline
    
    @property
    def time_left(self) -> float:
        """
        Returns time left in seconds
        """
        if not self.submitted_at:
            return 0.0
        
        return (self.deadline - self.submitted_at).total_seconds()
