from flask import Blueprint, redirect, render_template, request, url_for, session, send_from_directory

import os

from backend.progcomp import Progcomp

# from .adapters import GameUIAdapter
from .session import USERNAME_SESSION_KEY

# Initialise
pc = Progcomp()

bp = Blueprint("progcomp", __name__)

@bp.route("/")
def menu():
    session[USERNAME_SESSION_KEY] = ""
    return render_template("menu.html")

@bp.route("/start", methods=["POST"])
def start():
    """
    When someone hits the 'start' button
    """

    # Check username and password are in a valid format
    username = request.form.get("username")
    if username in [None, ""] or username.isspace() or len(username) > 100 or not username.isascii():
        return redirect(url_for("progcomp.menu"))
    
    password = request.form.get("password")
    print(password)
    if password in [None, ""] or password.isspace() or len(password) > 30 or not password.isascii():
        return redirect(url_for("progcomp.menu"))
    
    # Check password against potentially existing team
    team = pc.get_team(username)
    print(team)
    if team:
        if team.password != password:
            return redirect(url_for("progcomp.menu"))
    else:
        pc.add_team(username, password)
    
    # Save their username
    session[USERNAME_SESSION_KEY] = username

    return redirect(url_for("progcomp.submit"))

@bp.route("/submit", methods=["GET", "POST"])
def submit():
    """
    The submission page / home page for the contest
    """

    username = session.get(USERNAME_SESSION_KEY)
    if not username:
        return redirect(url_for("progcomp.menu"))
    # team = game.teams.get(username)

    return render_template("submissions.html", username=username)

    # List out team submission info

@bp.route("/problems/<string:name>", methods=["GET", "POST"])
def problem(name):
    """
    Retrieve the page for a problem
    """

    username = session.get(USERNAME_SESSION_KEY)
    if not username:
        return redirect(url_for("progcomp.menu"))
    
    pc.update_problems()

    problem = pc.get_problem(name)
    if not problem:
        return redirect(url_for("progcomp.submit"))

    return render_template("problem.html", username=username, problem=problem)

@bp.route("/download/pdf", methods=["GET", "POST"])
def dl_pdf(filename):
    """
    Download the main pdf
    """

    path = os.path.join(os.getcwd(), "pdf")
    return send_from_directory(path, "problems.txt", as_attachment=True)


@bp.route("/download/<string:p_name>/<string:filename>", methods=["GET", "POST"])
def download(p_name, filename):
    """
    Download a specified problem input
    """

    path = os.path.join(os.getcwd(), "problems", p_name, "input")
    if not os.path.exists(os.path.join(path, filename)):
        return redirect(url_for("progcomp.submit"))
    return send_from_directory(path, filename, as_attachment=True)

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