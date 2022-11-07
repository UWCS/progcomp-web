from flask import Blueprint, redirect, render_template, request, url_for, session

from backend.game import Player, AnswerType, PlayerState
from backend.repositories import QuestionBank, GameHistory
from backend.services import GameService

from .adapters import GameUIAdapter
from .session import USERNAME_SESSION_KEY

game_history = GameHistory()
question_bank = QuestionBank("test.csv")
game_service = GameService(game_history, question_bank)

bp = Blueprint("game", __name__)

@bp.route("/")
def menu():
    return render_template("menu.html")

@bp.route("/start", methods=["POST"])
def start():
    """
    When someone hits the 'start' button
    """

    username = request.form.get("username")
    if username is None or username == "" or username.isspace() or len(username) > 100:
        return redirect(url_for("game.menu"))
    
    # Save their username
    session[USERNAME_SESSION_KEY] = username
    
    # We would check if their team name already exists, if not make a team for them
    # prompt for creating/entering password? Could have been done in menu.html.
    game = game_service.new_game(num_qs=10, difficulty=-1)
    game.players[username] = Player(username)
    game_service.save_game(game.game_id)

    return redirect(url_for("game.submit", game_id=game.game_id))

@bp.route("/submit", methods=["GET", "POST"])
def submit():
    """
    The submission page / home page for the contest
    """

    username = session.get(USERNAME_SESSION_KEY)
    # team = game.teams.get(username)

    return render_template("submissions.html", username=username)

    # List out team submission info

# @bp.route("/problems/<string:game_id>", methods=["GET", "POST"])
# def problem(game_id):
#     """
#     Retrieve the page for a problem
#     """

#     # Attempt to get game information
#     game = game_service.get_game(game_id)
#     if game is None:
#         return "Game not found", 404

#     # Attempt to get player information
#     player_name = session.get(USERNAME_SESSION_KEY)
#     player = game.players.get(player_name)
    
#     if player is None:
#         return redirect(url_for("game.join", game_id=game_id))

#     if player.state is PlayerState.FINISHED:
#         return redirect(url_for("game.end", game_id=game_id))

#     if player.state is PlayerState.WAITING:
#         player.start_question_attempt(game.time_per_question)

#     # Did not submit an answer
#     if player.current_attempt.has_timed_out:
#         player.end_question_attempt(AnswerType.TIMEOUT)
#         return redirect(url_for("game.answer_outcome", game_id=game_id))

#     # Has submitted an answer
#     if request.method == "POST":
#         choice = GameUIAdapter.get_question_choice_selected(request.form)
#         correct_choice = GameUIAdapter.get_correct_answer_index(request.form)

#         if choice is None or correct_choice is None:
#             return "Something went wrong, no choice selected!", 500

#         game.on_question_answer(player, choice, correct_choice)

#         return redirect(url_for("game.answer_outcome", game_id=game_id))

#     choices, correct_index = game.questions[player.current_question].get_options()  

#     game_service.save_game(game_id)

#     return render_template(
#         "in_game.html",
#         game=game,
#         player=player,
#         current_question=game.questions[player.current_question],
#         choices=choices,
#         correct_index=correct_index
#     )

# @bp.route("/outcome/<string:game_id>", methods=["GET"])
# def answer_outcome(game_id):
#     """
#     For displaying the result of a question
#     """
#     game = game_service.get_game(game_id)

#     if game is None:
#         return "Game not found", 404

#     player_name = session.get(USERNAME_SESSION_KEY)
#     player = game.players.get(player_name)

#     if player is None:
#         return redirect(url_for("game.join", game_id=game_id))

#     if player.state is PlayerState.ANSWERING and player.current_attempt.has_timed_out:
#         player.end_question_attempt(AnswerType.TIMEOUT)

#     is_last_question = player.state == PlayerState.FINISHED

#     game_service.save_game(game_id)

#     return render_template(
#         "answer_outcome.html",
#         game=game,
#         player=player,
#         is_last_question=is_last_question
#     )

# @bp.route("/end/<string:game_id>", methods=["GET"])
# def end(game_id):
#     """
#     For displaying the game's end leaderboard
#     """
#     game = game_service.get_game(game_id)

#     if game is None:
#         return "Game not found", 404
    
#     return render_template(
#         "end.html",
#         game=game
#     )