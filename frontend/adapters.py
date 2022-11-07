from typing import Optional


class GameUIAdapter:
    @staticmethod
    def get_question_choice_selected(form: dict[str, str]) -> Optional[int]:
        """
        Gets choice selected by the user in the UI if it exists.

        :param form: payload of user request
        """
        return int(next((key.lstrip("choice_") for key in form.keys() if key.startswith("choice_")), None))

    @staticmethod
    def get_correct_answer_index(form: dict[str, str]) -> Optional[int]:
        return int(next((key.lstrip("correct_") for key in form.keys() if key.startswith("correct_")), None))