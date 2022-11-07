from typing import Optional
from random import choices
from datetime import timedelta


from .repositories import GameHistory, QuestionBank
from .game import Game


class GameService:
    def __init__(self, game_history: GameHistory, question_bank: QuestionBank) -> None:
        self.game_history = game_history
        self.question_bank = question_bank

    def new_game(self, num_qs: int = 10, difficulty: int = -1) -> Game:
        game = Game(
            self._generate_id(),
            self.question_bank.get_questions(num_qs, difficulty=difficulty),
            timedelta(seconds=20)
        )

        self.game_history.add_game(game)
        return game

    def get_game(self, game_id: str) -> Optional[Game]:
        return self.game_history.get_game_by_id(game_id)

    def save_game(self, game_id: str):
        pass

    def _generate_id(self) -> int:
        """
        Generate random hexadecimal string for a game id (5 characters)
        """
        return "".join(choices("0123456789ABCDEF", k=5))
