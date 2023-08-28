from flask import Flask, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime
from werkzeug.urls import url_parse
from ProjectFiles import app, db
from ProjectFiles.secFinancials import finSearch
from ProjectFiles.holderSearch import holderSearch
from ProjectFiles.forms import loginForm, RegistrationForm, newTaskForm, newContentForm, newNewsForm # pressReleaseForm, companyForm, contentForm, ideaForm
from ProjectFiles.models import userTable, taskTable, newsTable, eventTable, contentTable, peopleTable, exerciseTable, weightTable
from ProjectFiles.stockPrice import sp500

@app.route("/")
@app.route("/home")
def home():
    n = 8 # number of items to display in any given fieldset
    if current_user.is_authenticated:
        tasks = taskTable.query.filter_by(user_id=current_user.id).limit(n).all()
        contents = contentTable.query.filter_by(user_id=current_user.id).limit(n).all()
        newsItems = newsTable.query.filter_by(user_id=current_user.id).limit(n).all()
        time = datetime.now()  
        displayTime = time.strftime("%I:%M %p")
        sp = sp500()
        sp = f"{sp:.2f}"
        if displayTime.startswith("0"):
            displayTime = displayTime[1:]
        return render_template("home.html", tasks=tasks, contents=contents, newsItems=newsItems, time=displayTime, sp=sp)
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = loginForm()
    if form.validate_on_submit():
        user = userTable.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("home")
        return redirect(next_page)
    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = userTable(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You are now registered")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/about")
@login_required
def about():
    return render_template("about.html")

@app.route("/new_task", methods=["POST", "GET"])
@login_required
def new_task():
    form = newTaskForm()
    if form.validate_on_submit():
        taskCategory = form.taskCategory.data
        taskName = form.taskName.data
        taskLink = form.taskLink.data
        taskNote = form.taskNote.data
        task = taskTable(taskCategory=taskCategory, taskName=taskName, taskLink=taskLink, taskNote=taskNote, author=current_user)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("new_task.html", form=form)

@app.route("/update_task/<int:id>", methods=["POST", "GET"])
@login_required
def update_task(id):
    task = taskTable.query.get_or_404(id)
    if taskItem.author != current_user:
        flask("You are not authorized to update this item")
        return redirect(url_for("home"))
    form = newTaskForm()
    if form.validate_on_submit():
        task.taskCategory = form.taskCategory.data
        task.taskName = form.taskName.data
        task.taskLink = form.taskLink.data
        task.taskNote = form.taskNote.data
        db.session.commit()
        flash("Your task has been updated")
        return redirect(url_for("home"))
    elif request.method == "GET":
        form.taskCategory.data = task.taskCategory
        form.taskName.data = task.taskName
        form.taskLink.data = task.taskLink
        form.taskNote.data = task.taskNote
        return render_template("new_task.html", form=form)

@app.route("/delete_task/<int:id>")
@login_required
def delete_task(id):
    task = taskTable.query.get_or_404(id)
    if task.author == current_user:
        db.session.delete(task)
        db.session.commit()
        flash("Task successfully deleted")
        return redirect(url_for("home"))
    else:
        flash("User not authorized to delete")
        return redirect(url_for("home"))

@app.route("/new_content", methods=["POST", "GET"])
@login_required
def new_content():
    form = newContentForm()
    if form.validate_on_submit():
        newContent = contentTable(dateMade=form.dateMade.data, 
                                  contentType=form.contentType.data, 
                                  contentCreator=form.contentCreator.data, 
                                  contentLink=form.contentLink.data, 
                                  contentRating=form.contentRating.data, 
                                  contentSubject=form.contentSubject.data, 
                                  contentNote=form.contentNote.data, 
                                  author=current_user)
        db.session.add(newContent)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("new_content.html", form=form)

@app.route("/update_content/<int:id>", methods=["POST", "GET"])
@login_required
def update_content(id):
    contentItem = contentTable.query.get_or_404(id)
    if contentItem.author != current_user:
        flask("You are not authorized to update this item")
        return redirect(url_for("home"))
    form = newContentForm()
    if form.validate_on_submit():
        contentItem.dateMade = form.dateMade.data
        contentItem.contentType = form.contentType.data
        contentItem.contentCreator = form.contentCreator.data
        contentItem.contentLink = form.contentLink.data
        contentItem.contentRating = form.contentRating.data
        contentItem.contentSubject = form.contentSubject.data
        contentItem.contentNote = form.contentNote.data
        db.session.commit()
        flash("Your content has been updated")
        return redirect(url_for("home"))
    elif request.method == "GET":
        form.dateMade.data = contentItem.dateMade
        form.contentType.data = contentItem.contentType
        form.contentCreator.data = contentItem.contentCreator
        form.contentLink.data = contentItem.contentLink
        form.contentRating.data = contentItem.contentRating
        form.contentSubject.data = contentItem.contentSubject
        form.contentNote.data = contentItem.contentNote
        return render_template("new_content.html", form=form)

@app.route("/delete_content/<int:id>")
@login_required
def delete_content(id):
    contentItem = contentTable.query.get_or_404(id)
    if contentItem.author == current_user:
        db.session.delete(contentItem)
        db.session.commit()
        flash("Content successfully deleted")
        return redirect(url_for("home"))
    else:
        flash("User not authorized to delete")
        return redirect(url_for("home"))

#### News ####
@app.route("/new_news", methods=["POST", "GET"])
@login_required
def new_news():
    form = newNewsForm()
    if form.validate_on_submit():
        newNews = newsTable(newsType=form.newsType.data, 
                            newsTitle=form.newsTitle.data, 
                            newsNote=form.newsNote.data, 
                            newsLink=form.newsLink.data, 
                            newsTicker=form.newsTicker.data, 
                            newsDatePosted=form.newsDatePosted.data,
                            author=current_user)
        db.session.add(newNews)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("new_news.html", form=form)

@app.route("/update_news/<int:id>", methods=["POST", "GET"])
@login_required
def update_news(id):
    newsItem = newsTable.query.get_or_404(id)
    if newsItem.author != current_user:
        flash("You are not authorized to update this item")
        return redirect(url_for("home"))
    form = newNewsForm()
    if form.validate_on_submit():
        newsItem.newsType = form.newsType.data
        newsItem.newsTitle = form.newsTitle.data
        newsItem.newsNote = form.newsNote.data
        newsItem.newsLink = form.newsLink.data
        newsItem.newsTicker = form.newsTicker.data
        newsItem.newsDatePosted = form.newsDatePosted.data
        db.session.commit()
        flash("Your news item has been updated")
        return redirect(url_for("home"))
    elif request.method == "GET":
        form.newsType.data = newsItem.newsType
        form.newsTitle.data = newsItem.newsTitle
        form.newsNote.data = newsItem.newsNote
        form.newsLink.data = newsItem.newsLink
        form.newsTicker.data = newsItem.newsTicker
        form.newsDatePosted.data = newsItem.newsDatePosted
        return render_template("new_news.html", form=form)

@app.route("/delete_news/<int:id>")
@login_required
def delete_news(id):
    newsItem = newsTable.query.get_or_404(id)
    if newsItem.author == current_user:
        db.session.delete(newsItem)
        db.session.commit()
        flash("News item successfully deleted")
        return redirect(url_for("home"))
    else:
        flash("User not authorized to delete")
        return redirect(url_for("home"))

# @app.route("/pressRelease", methods=["POST", "GET"])
# def pressRelease():
#     pressReleaseList = None
#     form = pressReleaseForm()
#     if form.validate_on_submit():
#         contentDate = form.contentDate.data
#         company = form.company.data
#         ticker = form.ticker.data
#         link = form.link.data
#         product = form.product.data
#         pressReleaseList = {"contentDate": contentDate, "company": company, "ticker": ticker, "link": link}
#         # entry for date/time of the post itself
#         pressRelease = pressReleases(company=company, ticker=ticker, link=link, product=product, datePosted=contentDate)
#         db.session.add(pressRelease)
#         db.session.commit()
#         return render_template("pressRelease.html", pressReleaseList=pressReleaseList)
#     return render_template("pressRelease.html", form=form)

# @app.route("/events")
# def events():
#     return render_template("events.html")

# @app.route("/people")
# def people():
#     return render_template("people.html")

# @app.route("/companies", methods=["GET", "POST"])
# def companies():
#     companyInfo = None
#     form = companyForm()
#     if form.validate_on_submit():
#         ticker = form.ticker.data
#         startYear = form.startYear.data
#         holderCount = form.holderCount.data
#         companyName, financials, years = finSearch(ticker, startYear)
#         holderTable, last_row, CUSIP = holderSearch(ticker, holderCount)
#         companyInfo = {"companyName": companyName, "ticker": ticker}
#         return render_template("companies.html", companyInfo=companyInfo, financials=financials, years=years, holderTable=holderTable, last_row=last_row)
#     return render_template("companies.html", form=form, companyInfo=companyInfo)

# @app.route("/content", methods=["GET", "POST"])
# def content():
#     form = contentForm()
#     contents = Content.query.all()
#     if form.validate_on_submit():
#         dateMade = form.dateMade.data
#         contentType = form.contentType.data
#         contentCreator = form.contentCreator.data
#         contentLink = form.contentLink.data
#         contentNote = form.contentNote.data
#         contentRating = form.contentRating.data
#         # contentList = {"contentDate": contentDate, "ContentType": contentType, "creator": creator, "link": link}
#         contentItem = Content(dateMade=dateMade, contentType=contentType, contentLink=contentLink, contentCreator=contentCreator, contentNote=contentNote, contentRating=contentRating)
#         db.session.add(contentItem)
#         db.session.commit()
#         contents = Content.query.all()
#         return render_template("content.html", form=form, contents=contents)
#     return render_template("content.html", form=form, contents=contents)

# @app.route("/delete_content/<int:id>", methods=["GET", "POST"])
# def delete_content(id):
#     contentItem=Content.query.get_or_404(id)
#     db.session.delete(contentItem)
#     db.session.commit()
#     contents = Content.query.all()
#     return render_template("content.html", form=contentForm, contents=contents)

# @app.route("/content/<int:id>/update", methods=["GET", "POST"])
# def update_content(id):
#     contentItem = Content.query.get_or_404(id)
#     form = contentForm()
#     if form.validate_on_submit():
#         contentItem.dateMade = form.dateMade.data
#         contentItem.contentType = form.contentType.data
#         contentItem.contentCreator = form.contentCreator.data
#         contentItem.contentLink = form.contentLink.data
#         contentItem.contentNote = form.contentNote.data
#         contentItem.contentRating = form.contentRating.data
#         db.session.commit()
#         contents = Content.query.all()
#         flash("Your content has been updated", "success")
#         return render_template("content.html", form=form, contents=contents)
#     elif request.method == "GET":
#         form.dateMade.data = contentItem.dateMade
#         form.contentType.data = contentItem.contentType
#         form.contentCreator.data = contentItem.contentCreator
#         form.contentLink.data = contentItem.contentLink
#         form.contentNote.data = contentItem.contentNote
#         form.contentRating.data = contentItem.contentRating
#         contents = Content.query.all()
#     return render_template("content.html", form=form, contents=contents)

# @app.route("/ideas", methods=["GET", "POST"])
# def ideas():
#     form = ideaForm()
#     ideas = Ideas.query.all()
#     if form.validate_on_submit():
#         flash("Your item has been addded", "success")
#         category = form.category.data
#         link = form.link.data
#         note = form.note.data
#         idea = Ideas(category=category, link=link, note=note, status="New")
#         db.session.add(idea)
#         db.session.commit()
#         ideas = Ideas.query.all()
#         return render_template("ideas.html", form=form, ideas=ideas)
#     return render_template("ideas.html", form=form, ideas=ideas)

# @app.route("/delete_idea/<int:id>", methods=["GET", "POST"])
# def delete_idea(id):
#     idea=Ideas.query.get_or_404(id)
#     db.session.delete(idea)
#     db.session.commit()
#     ideas = Ideas.query.all()
#     return render_template("ideas.html", ideas=ideas, form=ideaForm())

# @app.route("/ideas/<int:id>/update", methods=["GET", "POST"])
# def update_idea(id):
#     idea = Ideas.query.get_or_404(id)
#     form = ideaForm()
#     if form.validate_on_submit():
#         idea.category = form.category.data
#         idea.link = form.link.data
#         idea.note = form.note.data
#         idea.status = form.status.data
#         idea.dateEdited = datetime.utcnow().date()
#         db.session.commit()
#         ideas = Ideas.query.all()
#         flash("Your item has been updated", "success")
#         return render_template("ideas.html", form=form, ideas=ideas)
#     elif request.method == "GET":
#         form.category.data = idea.category
#         form.link.data = idea.link
#         form.note.data = idea.note
#         form.status.data = idea.status
#     return render_template("updateIdea.html", form=form)