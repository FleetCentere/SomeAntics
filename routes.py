from flask import Flask, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from ProjectFiles import app, db
from ProjectFiles.secFinancials import finSearch
from ProjectFiles.holderSearch import holderSearch
from ProjectFiles.forms import pressReleaseForm, companyForm, loginForm, RegistrationForm, contentForm, ideaForm
from ProjectFiles.models import pressReleases, events, content, people, Users, Ideas

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
        pressRelease = pressReleases(company=company, ticker=ticker, link=link, product=product, datePosted=contentDate)
        db.session.add(pressRelease)
        db.session.commit()
        return render_template("pressRelease.html", pressReleaseList=pressReleaseList)
    return render_template("pressRelease.html", form=form)

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

@app.route("/content", methods=["GET", "POST"])
def content():
    contentList = None
    form = contentForm()
    if form.validate_on_submit():
        contentDate = form.contentDate.data
        contentType = form.contentType.data
        creator = form.creator.data
        link = form.link.data
        note = form.note.data
        contentRating = form.contentRating.data
        contentList = {"contentDate": contentDate, "ContentType": contentType, "creator": creator, "link": link}
        # entry for date/time of the post itself
        content = content(contentDate=contentDate, contentType=contentType, link=link, creator=creator, note=note, contentRating=contentRating)
        db.session.add(content)
        db.session.commit()
        return render_template("content.html", contentlist=contentlist)
    return render_template("content.html", form=form)

@app.route("/ideas", methods=["GET", "POST"])
def ideas():
    form = ideaForm()
    ideas = Ideas.query.all()
    if form.validate_on_submit():
        flash("Your item has been addded", "success")
        category = form.category.data
        link = form.link.data
        note = form.note.data
        idea = Ideas(category=category, link=link, note=note, status="New")
        db.session.add(idea)
        db.session.commit()
        ideas = Ideas.query.all()
        return render_template("ideas.html", form=form, ideas=ideas)
    return render_template("ideas.html", form=form, ideas=ideas)

@app.route("/delete_idea/<int:id>", methods=["GET", "POST"])
def delete_idea(id):
    idea=Ideas.query.get_or_404(id)
    db.session.delete(idea)
    db.session.commit()
    ideas = Ideas.query.all()
    return redirect(url_for("ideas"), ideas=ideas)

@app.route("/ideas/<int:id>/update", methods=["GET", "POST"])
def update_idea(id):
    idea = Ideas.query.get_or_404(id)
    form = ideaForm()
    if form.validate_on_submit():
        idea.category = form.category.data
        idea.link = form.link.data
        idea.note = form.note.data
        idea.status = form.status.data
        db.session.commit()
        ideas = Ideas.query.all()
        return redirect(url_for("ideas"), ideas=ideas)
    elif request.method == "GET":
        form.category.data = idea.category
        form.link.data = idea.link
        form.note.data = idea.note
        form.status.data = idea.status
    return render_template("updateIdea.html", form=form, idea=idea)


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