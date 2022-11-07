from enum import IntEnum
from datetime import datetime, timedelta
from .question import QuestionAttempt, AnswerType

class PlayerState(IntEnum):
    WAITING = 1
    ANSWERING = 2
    FINISHED = 3

class Player:
    def __init__(self, name: str):
        """
        Represents a Quiz player, and keeps track of their info
        """
        self.name: str = name
        self.current_question: int = 0

        self.score: int = 0
        self.current_streak: int = 0
        self.max_streak: int = 0
        self.num_correct: int = 0
        self.num_answered: int = 0

        self.current_attempt: QuestionAttempt = None
        self.state: PlayerState = PlayerState.WAITING

    def start_question_attempt(self, time_limit: timedelta) -> None:
        self.state = PlayerState.ANSWERING
        now = datetime.now()
        self.current_attempt = QuestionAttempt(now, now + time_limit)

    def end_question_attempt(self, outcome: AnswerType) -> None:
        if self.current_attempt is None:
            return
        
        self.current_attempt.submitted_at = datetime.now()
        self.current_attempt.outcome = outcome

        self.current_attempt.question_score = self.apply_scoring(outcome)
        
        self.state = PlayerState.WAITING
        self.current_question += 1

    # The scoring functions from week 2 are implemented below.
    
    def apply_scoring(self, outcome: AnswerType) -> int:
        """
        Updates player information based on a question's outcome and seconds remaining.
        Returns the points gained for this question.
        """
        if self.current_attempt is None:
            return 0

        self._update_tally(outcome)
        self._update_streaks(outcome)

        question_score = self._calculate_score(
            outcome=outcome,
            secs_left=self.current_attempt.time_left,
            current_streak=self.current_streak
        )

        self.score += question_score

        return question_score
    
    def _update_tally(self: "Player", outcome: AnswerType):
        # Updates the number of questions both attempted and correct
        if outcome == AnswerType.CORRECT:
            self.num_answered += 1
            self.num_correct += 1
        elif outcome == AnswerType.INCORRECT:
            self.num_answered += 1
    
    def _update_streaks(self: "Player", outcome: AnswerType):
        # Updates the current and maximum streaks
        if outcome == AnswerType.CORRECT:
            self.current_streak += 1
            
            if self.current_streak > self.max_streak:
                self.max_streak = self.current_streak
        else:
            self.current_streak = 0
    
    def _calculate_score(self: "Player", outcome: AnswerType, secs_left: float, current_streak: int) -> int:
        # Calculates the score for a given question.
        if outcome != AnswerType.CORRECT:
            return 0
        
        # 1000 pts at 20.0, 0 pts at 0.0, decreases linearly
        time_score = int(secs_left * 50)

        # Increases by 200 pts each time for 2+ streak
        streak_score = (current_streak - 1) * 200

        return time_score + streak_score
