import glob
import logging
import os
import re
from datetime import datetime
from typing import Union

from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from werkzeug.utils import secure_filename
from werkzeug.wrappers.response import Response

FlaskResponse = Union[Response, str]

from .database import db
from .models import *

# from .adapters import GameUIAdapter
from .session import PROGCOMP_SESSION_KEY, USERNAME_SESSION_KEY


def get_pc() -> Progcomp:
    name = session.get(PROGCOMP_SESSION_KEY)
    pc = db.session.query(Progcomp).where(Progcomp.name == name).first()
    return pc


bp = Blueprint("progcomp", __name__)


@bp.route("/")
def menu() -> FlaskResponse:
    username = session.get(USERNAME_SESSION_KEY, "main")
    if (pc := get_pc()) is None:
        return redirect(url_for("progcomp.progcomps"))
    return render_template("menu.html", progcomp=pc, username=username)


def partition(items: list, func: Callable, order=[]) -> list:
    results = defaultdict(list)
    for item in order:
        results[item] = []
    for item in items:
        results[func(item)].append(item)
    print(results)
    return results


@bp.route("/progcomps")
def progcomps() -> FlaskResponse:
    session[PROGCOMP_SESSION_KEY] = None
    username = session.get(USERNAME_SESSION_KEY, "main")
    pcs = db.session.query(Progcomp).all()
    pcs = [pc for pc in pcs if pc.visible]

    parts = partition(pcs, lambda pc: pc.category, ["Upcoming", "Active", "Complete"])
    if parts["Unknown"]:
        logging.warning(f"Progcomps with unknown times: {parts['Unknown']}")
    return render_template(
        "progcomps.html",
        partitions=parts if pcs else {},
        progcomp=get_pc(),
        username=username,
    )


@bp.route("/progcomp/clear")
def clear_progcomp() -> FlaskResponse:
    session[PROGCOMP_SESSION_KEY] = None
    session[USERNAME_SESSION_KEY] = None

    return redirect(url_for("progcomp.progcomps"))


@bp.route("/progcomp/<string:pc_name>")
def set_progcomp(pc_name) -> FlaskResponse:
    if db.session.query(Progcomp).where(Progcomp.name == pc_name).first():
        session[PROGCOMP_SESSION_KEY] = pc_name
        session[USERNAME_SESSION_KEY] = None

    return redirect(url_for("progcomp.menu"))


def verify_input(inp: Optional[str], max_len: int = 100) -> bool:
    return not (
        inp is None
        or inp == ""
        or inp.isspace()
        or len(inp) > max_len
        or not inp.isalnum()
    )


@bp.route("/start", methods=["POST"])
def start() -> FlaskResponse:
    """
    When someone hits the 'start' button
    """

    if (pc := get_pc()) is None:
        return redirect(url_for("progcomp.progcomps"))

    # Check username and password are in a valid format
    username = request.form.get("username")
    if username is None or not verify_input(username, 100):
        return redirect(url_for("progcomp.menu"))

    password = request.form.get("password")
    if password is None or not verify_input(password, 30):
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

    return redirect(url_for("progcomp.submissions"))


@bp.route("/logout", methods=["POST"])
def logout() -> FlaskResponse:
    """
    When someone hits the 'logout' button
    """

    # Save their username
    session[USERNAME_SESSION_KEY] = None

    return redirect(url_for("progcomp.menu"))


@bp.route("/submissions", methods=["GET"])
def submissions() -> FlaskResponse:
    """
    The submission page / home page for the contest
    """

    if (pc := get_pc()) is None:
        return redirect(url_for("progcomp.progcomps"))

    username = session.get(USERNAME_SESSION_KEY)
    if not username:
        return redirect(url_for("progcomp.menu"))
    team = pc.get_team(username)
    if not team:
        return redirect(url_for("progcomp.menu"))

    # List out team submission info
    return render_template(
        "submissions.html", team=team, progcomp=pc, username=username
    )


@bp.route("/problems/<string:p_name>", methods=["GET", "POST"])
def problem(p_name) -> FlaskResponse:
    """
    Retrieve the page for a problem
    """
    if (pc := get_pc()) is None:
        return redirect(url_for("progcomp.progcomps"))

    username = session.get(USERNAME_SESSION_KEY)
    if not username:
        return redirect(url_for("progcomp.menu"))

    problem = pc.get_problem(p_name)
    if not problem or not problem.visible:
        return redirect(url_for("progcomp.submissions"))

    if request.method == "POST":
        if not problem.open:
            return redirect(request.url)
        # TODO: Multiple files (script + output data at the same time)
        # check if the post request has the file part

        if "output" not in request.files or "script" not in request.files:
            return redirect(request.url)

        # If user doesn't select a file, browser submits empty file.
        output = request.files.get("output")
        if not output or output.filename == "":
            return redirect(request.url)

        script = request.files.get("script")
        if not script or script.filename is None or script.filename == "":
            return redirect(request.url)
        script_name = secure_filename(script.filename)

        test = request.form.get("test_select")
        if not test:
            return redirect(request.url)

        time = datetime.now()
        time_str = time.strftime("%Y-%m-%d_%H-%M-%S")

        # need to folder w/ timestamp on path
        path = os.path.join(
            os.getcwd(), "submissions", username, p_name, test, time_str
        )

        os.makedirs(path, exist_ok=True)

        # Upload files
        output.save(os.path.join(path, "output.txt"))
        script.save(os.path.join(path, script_name))

        pc.make_submission(path, username, p_name, test, timestamp=time)

        return redirect(url_for("progcomp.submissions"))

    return render_template(
        "problem.html", username=username, problem=problem, progcomp=pc
    )


@bp.route("/download/pdf", methods=["GET"])
def dl_pdf() -> FlaskResponse:
    """
    Download the main pdf
    """

    if (pc := get_pc()) is None:
        return redirect(url_for("progcomp.progcomps"))

    return send_from_directory(
        os.path.join(os.getcwd(), "problems", pc.name),
        "problems.pdf",
        as_attachment=True,
    )


@bp.route("/download/<string:p_name>/<string:filename>", methods=["GET"])
def download(p_name, filename) -> FlaskResponse:
    """
    Download a specified problem input
    """

    if (pc := get_pc()) is None:
        return redirect(url_for("progcomp.progcomps"))

    path = os.path.join(os.getcwd(), "problems", pc.name, p_name, "input")
    if not os.path.exists(os.path.join(path, filename)):
        return redirect(url_for("progcomp.submissions"))
    return send_from_directory(path, filename, as_attachment=True)


@bp.route("/leaderboard", methods=["GET"])
def leaderboard_main() -> FlaskResponse:

    if (pc := get_pc()) is None:
        return redirect(url_for("progcomp.progcomps"))

    print("SHOW LEADEDBOARD", pc.show_leaderboard)
    if not pc.show_leaderboard:
        return redirect(url_for("progcomp.menu"))

    scores = pc.score_teams()
    username = session.get(USERNAME_SESSION_KEY)
    return render_template(
        "leaderboard_hub.html",
        problems=[p for p in pc.visible_problems if p.name != "0"],
        scores=scores,
        progcomp=pc,
        username=username,
    )


@bp.route("/leaderboard/<string:p_name>/<string:p_set>", methods=["GET"])
def leaderboard(p_name, p_set) -> FlaskResponse:
    if (pc := get_pc()) is None:
        return redirect(url_for("progcomp.progcomps"))

    if (
        not pc.show_leaderboard
        or not re.match(r"^[A-Za-z0-9_]+$", p_name)
        or not re.match(r"^[A-Za-z0-9_]+$", p_name)
    ):
        return redirect(url_for("progcomp.menu"))

    problem: Optional[Problem] = pc.get_problem(p_name)
    if not problem:
        return redirect(url_for("progcomp.menu"))
    test: Optional[Test] = problem.get_test(p_set)
    if test is None or not test:
        return redirect(url_for("progcomp.menu"))

    subs = test.ranked_submissions
    username = session.get(USERNAME_SESSION_KEY)
    return render_template(
        "leaderboard.html",
        p_name=p_name,
        p_set=p_set,
        submissions=subs,
        progcomp=pc,
        username=username,
    )


@bp.route("/poll", methods=["GET"])
def poll() -> FlaskResponse:
    if (pc := get_pc()) is None:
        return jsonify({})

    data = {"end_time": pc.end_time.timestamp() if pc.end_time else 0}
    return jsonify(data)
