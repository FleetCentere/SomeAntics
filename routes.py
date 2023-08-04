from flask import Flask, render_template, url_for, redirect, request
from ProjectFiles import app #, db


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")