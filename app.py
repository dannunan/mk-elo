from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/submit")
def submit():
    return render_template("submit.html")


@app.route("/submit_scores")
def submit_scores():
    return render_template("submit_scores.html")
