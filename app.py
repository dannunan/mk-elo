"""Flask application."""

from flask import Flask, render_template, session, request, redirect, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = b"temporary key"

TEMP_PW = {"user": generate_password_hash("password")}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        if username is None:
            error = "Incorrect username"
        elif not check_password_hash(TEMP_PW["user"], password):
            error = "Incorrect password"

        if error is None:
            session.clear()
            session["username"] = username
            app.logger.info("%s logged in", username)
            return redirect(url_for("submit"))

        flash(error)

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/submit", methods=["GET", "POST"])
def submit():
    if "username" not in session:
        return redirect("login")
    if request.method == "POST":
        session["n_players"] = int(request.form["n_players"])
        session["n_races"] = int(request.form["n_races"])
        return redirect("submit_scores")
    return render_template("submit.html")


@app.route("/submit_scores", methods=["GET", "POST"])
def submit_scores():
    if "username" not in session:
        return redirect("login")
    if "n_players" not in session:
        return redirect("submit")
    if request.method == "POST":
        # TODO get for variable number of players
        player = request.form["player"]
        score = int(request.form["score"])

        app.logger.info("Submitted result for %s", player)

        # TODO: update db and trigger rating adjustment
        return redirect("/")
    return render_template("submit_scores.html")
