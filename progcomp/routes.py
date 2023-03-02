import glob
import logging
import os
import re
from datetime import datetime

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from werkzeug.utils import secure_filename

from .database import db
from .models import *

# from .adapters import GameUIAdapter
from .session import USERNAME_SESSION_KEY

# pc: Progcomp = None


def load_pc():
    # with app.app_context():
    pc = db.session.query(Progcomp).first()
    if not pc:
        db.session.add(pc := Progcomp(name="main"))
        db.session.commit()
    # pc.update_problems()
    db.session.flush()


def get_pc():
    return db.session.query(Progcomp).first()


bp = Blueprint("progcomp", __name__)


@bp.route("/")
def menu():
    username = session.get(USERNAME_SESSION_KEY)
    return render_template("menu.html", progcomp=get_pc(), username=username)


@bp.route("/start", methods=["POST"])
def start():
    """
    When someone hits the 'start' button
    """

    # Check username and password are in a valid format
    username = request.form.get("username")
    if (
        username in [None, ""]
        or username.isspace()
        or len(username) > 100
        or not username.isalnum()
    ):
        return redirect(url_for("progcomp.menu"))

    password = request.form.get("password")
    if (
        password in [None, ""]
        or password.isspace()
        or len(password) > 30
        or not password.isascii()
    ):
        return redirect(url_for("progcomp.menu"))

    # Check password against potentially existing team
    team = get_pc().get_team(username)
    print("Team", team)
    if team:
        if team.password != password:
            return redirect(url_for("progcomp.menu"))
    else:
        get_pc().add_team(username, password)

    # Save their username
    session[USERNAME_SESSION_KEY] = username

    return redirect(url_for("progcomp.submit"))


@bp.route("/logout", methods=["POST"])
def logout():
    """
    When someone hits the 'logout' button
    """

    # Save their username
    session[USERNAME_SESSION_KEY] = None

    return redirect(url_for("progcomp.menu"))


@bp.route("/submit", methods=["GET"])
def submit():
    """
    The submission page / home page for the contest
    """

    username = session.get(USERNAME_SESSION_KEY)
    if not username:
        return redirect(url_for("progcomp.menu"))
    pc = get_pc()
    team = pc.get_team(username)
    if not team or pc.freeze:
        return redirect(url_for("progcomp.menu"))

    # List out team submission info
    return render_template("submissions.html", team=team, progcomp=get_pc())


@bp.route("/problems/<string:p_name>", methods=["GET", "POST"])
def problem(p_name):
    """
    Retrieve the page for a problem
    """

    username = session.get(USERNAME_SESSION_KEY)
    if not username:
        return redirect(url_for("progcomp.menu"))

    # get_pc().update_problems()

    problem = get_pc().get_problem(p_name)
    if not problem:
        return redirect(url_for("progcomp.submit"))

    if request.method == "POST":
        # TODO: Multiple files (script + output data at the same time)
        # check if the post request has the file part

        if "output" not in request.files or "script" not in request.files:
            return redirect(request.url)

        # If user doesn't select a file, browser submits empty file.
        output = request.files.get("output")
        if not output or output.filename == "":
            return redirect(request.url)

        script = request.files.get("script")
        if not script or script.filename == "":
            return redirect(request.url)
        script_name = secure_filename(script.filename)

        test = request.form.get("test_select")
        if not test:
            return redirect(request.url)

        time = datetime.now()
        time_str = get_pc().get_timestamp_str(time)

        # need to folder w/ timestamp on path
        path = os.path.join(
            os.getcwd(), "submissions", username, p_name, test, time_str
        )

        os.makedirs(path, exist_ok=True)

        # Upload files
        output.save(os.path.join(path, "output.txt"))
        script.save(os.path.join(path, script_name))

        get_pc().make_submission(path, username, p_name, test, timestamp=time)

        return redirect(url_for("progcomp.submit"))

    return render_template(
        "problem.html", username=username, problem=problem, progcomp=get_pc()
    )


@bp.route("/download/pdf", methods=["GET"])
def dl_pdf():
    """
    Download the main pdf
    """

    return send_from_directory(os.getcwd(), "problems.pdf", as_attachment=True)


@bp.route("/download/<string:p_name>/<string:filename>", methods=["GET"])
def download(p_name, filename):
    """
    Download a specified problem input
    """

    path = os.path.join(os.getcwd(), "problems", p_name, "input")
    if not os.path.exists(os.path.join(path, filename)):
        return redirect(url_for("progcomp.submit"))
    return send_from_directory(path, filename, as_attachment=True)


@bp.route("/leaderboard", methods=["GET"])
def leaderboard_main():
    print("SHOW LEADEDBOARD", get_pc().show_leaderboard)
    if not get_pc().show_leaderboard:
        return redirect(url_for("progcomp.menu"))

    pc = get_pc()
    scores = pc.score_teams()
    # if not pc.freeze:
    #     scores = []
    return render_template(
        "leaderboard_hub.html",
        problems=[p for p in get_pc().enabled_problems if p.name != "0"],
        scores=scores,
        progcomp=get_pc(),
    )


@bp.route("/leaderboard/<string:p_name>/<string:p_set>", methods=["GET"])
def leaderboard(p_name, p_set):
    if (
        not get_pc().show_leaderboard
        or not re.match(r"^[A-Za-z0-9_]+$", p_name)
        or not re.match(r"^[A-Za-z0-9_]+$", p_name)
    ):
        return redirect(url_for("progcomp.menu"))

    problem: Problem = get_pc().get_problem(p_name)
    if not problem:
        return
    test: Test = problem.get_test(p_set)
    if not test:
        return

    subs = test.ranked_submissions

    return render_template(
        "leaderboard.html",
        p_name=p_name,
        p_set=p_set,
        submissions=subs,
        progcomp=get_pc(),
    )
