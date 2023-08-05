from flask import Flask, render_template, url_for, redirect, request, flash
from ProjectFiles import app #, db


messages = [{"title": "First Message", "content": "First message content"}, {"title": "Second message", "content": "Second message content"}]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", messages=messages)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Title is required")
        elif not content:
            flash("Content is required")
        else:
            messages.append({"title": title, "content": content})
            return redirect(url_for("home"))
    return render_template("create.html")