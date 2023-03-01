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

pc: Progcomp = None


def load_pc():
    global pc
    # with app.app_context():
    pc = db.session.query(Progcomp).first()
    if not pc:
        db.session.add(pc := Progcomp(name="main"))
        db.session.commit()
    pc.update_problems()
    db.session.flush()


bp = Blueprint("progcomp", __name__)


@bp.route("/")
def menu():
    return render_template("menu.html", progcomp=pc)


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
    team = pc.get_team(username)
    print("Team", team)
    if team:
        if team.password != password:
            return redirect(url_for("progcomp.menu"))
    else:
        pc.add_team(username, password)

    # Save their username
    session[USERNAME_SESSION_KEY] = username

    return redirect(url_for("progcomp.submit"))


@bp.route("/submit", methods=["GET"])
def submit():
    """
    The submission page / home page for the contest
    """

    username = session.get(USERNAME_SESSION_KEY)
    if not username:
        return redirect(url_for("progcomp.menu"))
    team = pc.get_team(username)
    if not team:
        return redirect(url_for("progcomp.menu"))

    # List out team submission info
    return render_template("submissions.html", team=team, progcomp=pc)


@bp.route("/problems/<string:p_name>", methods=["GET", "POST"])
def problem(p_name):
    """
    Retrieve the page for a problem
    """

    username = session.get(USERNAME_SESSION_KEY)
    if not username:
        return redirect(url_for("progcomp.menu"))

    # pc.update_problems()

    problem = pc.get_problem(p_name)
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
        time_str = pc.get_timestamp_str(time)

        # need to folder w/ timestamp on path
        path = os.path.join(
            os.getcwd(), "submissions", username, p_name, test, time_str
        )

        os.makedirs(path, exist_ok=True)

        # Upload files
        output.save(os.path.join(path, "output.txt"))
        script.save(os.path.join(path, script_name))

        pc.make_submission(path, username, p_name, test, timestamp=time)

        return redirect(url_for("progcomp.submit"))

    return render_template(
        "problem.html", username=username, problem=problem, progcomp=pc
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
    if not pc.show_leaderboard:
        return redirect(url_for("progcomp.menu"))
    problems = []
    for dir in glob.glob(os.path.join(os.getcwd(), "results/*")):
        if not os.path.isdir(dir):
            continue
        p = Problem(dir.split("/")[-1], False)
        problems.append(p)
        for filen in glob.glob(dir + "/*.txt"):
            p.test_names.append(filen.split("/")[-1][:-4])
    problems.sort(key=lambda p: p.name)

    with open(os.path.join(os.getcwd(), f"results/winners.txt")) as f:
        lines = f.readlines()
    winners = []
    for line in lines:
        parts = [x.strip() for x in re.split(r" +", line.strip())]
        winners.append(parts)

    top3 = f"{winners[0][0]}, {winners[1][0]}, and {winners[2][0]}"
    return render_template(
        "leaderboard_hub.html",
        problems=problems,
        winners=winners,
        top3=top3,
        progcomp=pc,
    )


@bp.route("/leaderboard/<string:p_name>/<string:p_set>", methods=["GET"])
def leaderboard(p_name, p_set):
    if not pc.show_leaderboard:
        return redirect(url_for("progcomp.menu"))

    # pc.update_problems()
    # problem = pc.get_problem(p_name)
    # print(problem, repr(p_set), repr(problem.test_names))
    # if not problem or (p_set + ".txt") not in problem.test_names:
    # return redirect(url_for("progcomp.submit"))

    if not p_name.isalnum() or not p_set.isalnum():
        return
    try:
        with open(os.path.join(os.getcwd(), f"results/{p_name}/{p_set}.txt")) as f:
            lines = f.readlines()
    except FileNotFoundError:
        return redirect(url_for("progcomp.leaderboard_main"))

    this_round = set()
    results = []
    for line in lines:
        parts = [x.strip() for x in re.split(r" +", line.strip())]

        if parts[3] not in this_round:
            print(parts)
            if parts[2] == "[CORRECT]" or parts[2] == "[PARTIAL]":
                sub = Submission(
                    Team(parts[3], ""), p_name, parts[1].split(".")[0], p_set, parts[0]
                )
                sub.status = parts[2][1:-1]
                results.append(sub)
                # print(results[-1])
                this_round.add(parts[3])

    return render_template(
        "leaderboard.html",
        p_name=p_name,
        p_set=p_set,
        submissions=results,
        progcomp=pc,
    )
