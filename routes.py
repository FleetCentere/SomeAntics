from flask import Flask, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from ProjectFiles import app, db
from ProjectFiles.secFinancials import finSearch
from ProjectFiles.holderSearch import holderSearch
from ProjectFiles.forms import pressReleaseForm, companyForm, loginForm, RegistrationForm
from ProjectFiles.models import pressReleases, events, content, people, Users

messages = [{"title": "First Message", "content": "First message content"}, 
            {"title": "Second message", "content": "Second message content"}]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", messages=messages)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = loginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("home")
        return redirect(next_page)
    return render_template("login.html", form=form)

@app.route("/about")
@login_required
def about():
    return render_template("about.html")

@app.route("/pressRelease", methods=["POST", "GET"])
def pressRelease():
    pressReleaseList = None
    form = pressReleaseForm()
    if form.validate_on_submit():
        contentDate = form.contentDate.data
        company = form.company.data
        ticker = form.ticker.data
        link = form.link.data
        product = form.product.data
        pressReleaseList = {"contentDate": contentDate, "company": company, "ticker": ticker, "link": link}
        # entry for date/time of the post itself
    return render_template("pressRelease.html", form=form, pressReleaseList=pressReleaseList)

@app.route("/events")
def events():
    return render_template("events.html")

@app.route("/people")
def people():
    return render_template("people.html")

@app.route("/companies", methods=["GET", "POST"])
def companies():
    companyInfo = None
    form = companyForm()
    if form.validate_on_submit():
        ticker = form.ticker.data
        startYear = form.startYear.data
        holderCount = form.holderCount.data
        companyName, financials, years = finSearch(ticker, startYear)
        holderTable, last_row, CUSIP = holderSearch(ticker, holderCount)
        companyInfo = {"companyName": companyName, "ticker": ticker}
        return render_template("companies.html", companyInfo=companyInfo, financials=financials, years=years, holderTable=holderTable, last_row=last_row)
    return render_template("companies.html", form=form, companyInfo=companyInfo)

@app.route("/content")
def content():
    return render_template("content.html")

@app.route("/ideas")
def ideas():
    return render_template("ideas.html")

@app.route("/logout")
def logout():
    logout_user()
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You are now registered")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)