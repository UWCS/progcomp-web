from datetime import timedelta
from .question import Question, AnswerType
from .player import Player, PlayerState


class Game:
    def __init__(self, game_id: str, questions: list[Question], time_per_question: timedelta):
        """
        Represents the state of a game

        :param game_id: the unique id of the game
        :param questions: questions to be asked in order
        :param time_per_question: time per question as a `timedelta`
        """
        self.game_id = game_id
        self.questions = questions
        self.time_per_question = time_per_question

        self.players = {}

    @property
    def num_questions(self) -> int:
        return len(self.questions)

    @property
    def num_players(self) -> int:
        return len(self.players)

    def on_question_answer(self, player: Player, choice: int, correct_choice: int):
        if choice == correct_choice:
            outcome = AnswerType.CORRECT
        else:
            outcome = AnswerType.INCORRECT

        player.end_question_attempt(outcome)

        if self.has_player_finished(player):
            player.state = PlayerState.FINISHED

    def has_player_finished(self, player: Player) -> bool:
        return player.current_question >= self.num_questions

    def get_leaderboard(self) -> list[Player]:
        # TODO: make O(horrible) to fix in week 6, such as bubble sort
        return sorted(
            self.players.values(),
            key=lambda p: (p.score, p.max_streak, p.num_correct, p.name),
            reverse=True
        )