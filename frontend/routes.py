from flask import Blueprint, redirect, render_template, request, url_for, session, send_from_directory, flash
from werkzeug.utils import secure_filename
import os

from backend.progcomp import Progcomp

# from .adapters import GameUIAdapter
from .session import USERNAME_SESSION_KEY

# Initialise
pc = Progcomp()

bp = Blueprint("progcomp", __name__)

@bp.route("/")
def menu():
    # session[USERNAME_SESSION_KEY] = ""
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
    return render_template("submissions.html", team=team)

    

@bp.route("/problems/<string:p_name>", methods=["GET", "POST"])
def problem(p_name):
    """
    Retrieve the page for a problem
    """

    username = session.get(USERNAME_SESSION_KEY)
    if not username:
        return redirect(url_for("progcomp.menu"))
    
    pc.update_problems()

    problem = pc.get_problem(p_name)
    if not problem:
        return redirect(url_for("progcomp.submit"))
    
    if request.method == 'POST':
        print("Uploading file")
        # TODO: Multiple files (script + output data at the same time)
        # check if the post request has the file part
        print(request.files)
        if 'file' not in request.files:
            print("no file part")
            return redirect(request.url)
        file = request.files['file']
        # If user doesn't select a file, browser submits empty file.
        print(file)
        if not file or file.filename == '':
            return redirect(request.url)
        filename = secure_filename(file.filename)
        print("Uploaded file")
        
        # need to add folder w/ timestamp on path!
        path = os.path.join(os.getcwd(), "submissions", username, "00_00_00", p_name)
        # intermediate directories need to be made
        os.makedirs(path, exist_ok=True)
        file.save(os.path.join(path, filename))
        return redirect(url_for('progcomp.submit'))
    
    return render_template("problem.html", username=username, problem=problem)


@bp.route("/download/pdf", methods=["GET"])
def dl_pdf(filename):
    """
    Download the main pdf
    """

    path = os.path.join(os.getcwd(), "pdf")
    return send_from_directory(path, "problems.txt", as_attachment=True)


@bp.route("/download/<string:p_name>/<string:filename>", methods=["GET"])
def download(p_name, filename):
    """
    Download a specified problem input
    """

    path = os.path.join(os.getcwd(), "problems", p_name, "input")
    if not os.path.exists(os.path.join(path, filename)):
        return redirect(url_for("progcomp.submit"))
    return send_from_directory(path, filename, as_attachment=True)