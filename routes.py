from flask import Flask, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import desc
from datetime import datetime, date, timedelta
from werkzeug.urls import url_parse
from ProjectFiles import app, db
from ProjectFiles.secFinancials import finSearch
from ProjectFiles.holderSearch import holderSearch
from ProjectFiles.forms import loginForm, RegistrationForm, editProfileForm, newTaskForm, newContentForm, newNewsForm, newEventForm, ideasForm, dailyForm, newExerciseForm
from ProjectFiles.models import userTable, dayTable, taskTable, newsTable, eventTable, contentTable, exerciseTable, peopleEvents, personsTable, ideaTable
from ProjectFiles.stockPrice import sp500

@app.route("/")
@app.route("/home")
def home():
    n = 8 # number of items to display in any given fieldset
    if current_user.is_authenticated:
        tasks = taskTable.query.filter_by(user_id=current_user.id).limit(n).all()
        contents = contentTable.query.filter_by(user_id=current_user.id).limit(n).all()
        newsItems = newsTable.query.filter_by(user_id=current_user.id).limit(n).all()
        events = eventTable.query.filter_by(user_id=current_user.id).limit(n).all()
        current = datetime.now()
        displayTime = current.strftime("%I:%M %p")
        displayDay = f"{current.strftime('%A')} {current.month}/{current.day}/{current.year}"
        sp = sp500()
        user = current_user
        if displayTime.startswith("0"):
            displayTime = displayTime[1:]
        return render_template("home.html", user=user, tasks=tasks, contents=contents, newsItems=newsItems, events=events, displayTime=displayTime, displayDay=displayDay, sp=sp)
    return redirect(url_for("login"))

@app.route("/daily_form", methods=["GET", "POST"])
@login_required
def daily_form():
    n = 20
    latest_date = datetime.now() - timedelta(days=n)
    days = db.session.query(dayTable).filter(dayTable.date >= latest_date)
    days = days.order_by(desc(dayTable.date)).all()
    counts_dict = {}
    for day in days:
        counts_dict[day] = {"exercise": db.session.query(exerciseTable).filter(exerciseTable.day_id == day.id).filter(exerciseTable.user_id == current_user.id).count(),
                            "contents": db.session.query(contentTable).filter(contentTable.day_id == day.id).filter(contentTable.user_id == current_user.id).count(),
                            "events": db.session.query(eventTable).filter(eventTable.day_id == day.id).filter(eventTable.user_id == current_user.id).count(),
                            "news": db.session.query(newsTable).filter(newsTable.day_id == day.id).filter(newsTable.user_id == current_user.id).count()}
    form = dailyForm()
    current = datetime.now()
    displayTime = current.strftime("%I:%M %p")
    if displayTime.startswith("0"):
        displayTime = displayTime[1:]
    displayDay = f"{current.strftime('%A')[:3]} {current.month}/{current.day}/{current.year}"
    sp = sp500()
    if request.method == "GET":
        time = datetime.now()
        today = time.date()
        todayEntry = dayTable.query.filter_by(date=today, user_id=current_user.id).first()
        if todayEntry == None:
            return render_template("daily_form.html", counts_dict=counts_dict, days=days, user=current_user, form=form, displayTime=displayTime, displayDay=displayDay, sp=sp)
        else:
            form.date.data = todayEntry.date
            form.weight.data = todayEntry.weight
            form.sleep.data = todayEntry.sleep
            form.morning.data = todayEntry.morning
            form.afternoon.data = todayEntry.afternoon
            form.evening.data = todayEntry.evening
            form.journal.data = todayEntry.journal
            return render_template("daily_form.html", counts_dict=counts_dict, days=days, user=current_user, form=form, displayTime=displayTime, displayDay=displayDay, sp=sp)
    if form.validate_on_submit():
        # collect input
        date = form.date.data
        weight = form.weight.data
        sleep = form.sleep.data
        morning = form.morning.data
        afternoon = form.afternoon.data
        evening = form.evening.data
        journal = form.journal.data

        # add to day table
        todayEntry = dayTable.query.filter_by(date=date, user_id=current_user.id).first()
        if todayEntry == None:
            newEntry = dayTable(date=date, weight=weight, sleep=sleep, morning=morning, afternoon=afternoon, evening=evening, journal=journal, author=current_user)
            db.session.add(newEntry)
            flash("Your daily items have been submitted")
        else:
            todayEntry.weight = form.weight.data
            todayEntry.sleep = form.sleep.data
            todayEntry.morning = form.morning.data
            todayEntry.afternoon = form.afternoon.data
            todayEntry.evening = form.evening.data
            todayEntry.journal = form.journal.data
            flash("Your daily items have been updated")
        db.session.commit()
        return redirect(url_for("daily_form"))

@app.route("/daily_content", methods=["GET", "POST"])
@login_required
def daily_content():
    total_days = 10
    latest_date = datetime.now() - timedelta(days=total_days)
    days = db.session.query(dayTable).filter(dayTable.date >= latest_date)
    days = days.order_by(desc(dayTable.date)).all()
    form = newContentForm()
    contents = contentTable.query.filter_by(user_id=current_user.id).all()
    category_tuple = db.session.query(contentTable.contentType).distinct().all()
    categories = [category[0] for category in category_tuple]
    content_dict = {}
    for day in days:
        content_dict[day.date] = {}
        for category in categories:
            content_dict[day.date][category] = contentTable.query.filter(contentTable.day == day, contentTable.contentType == category).count()
    if form.validate_on_submit():
        day = dayTable.query.filter_by(date=form.dateConsumed.data).first()
        if day == None:
            day = dayTable(date=form.dateConsumed.data, author=current_user)
            db.session.add(day)
        newContent = contentTable(dateConsumed=form.dateConsumed.data, dateMade=form.dateMade.data, contentType=form.contentType.data, contentCreator=form.contentCreator.data, contentLink=form.contentLink.data, contentRating=form.contentRating.data, contentSubject=form.contentSubject.data, contentNote=form.contentNote.data, author=current_user, day=day)
        db.session.add(newContent)
        db.session.commit()
        flash("Your content has been added")
        return redirect(url_for("daily_form"))
    return render_template("daily_content.html", user=current_user, form=form, content_dict=content_dict, categories=categories)

@app.route("/daily_exercise", methods=["GET", "POST"])
@login_required
def daily_exercise():
    form = newExerciseForm()
    if form.validate_on_submit():
        day = dayTable.query.filter_by(date=form.exerciseDate.data).first()
        if day == None:
            day = dayTable(date=form.dateConsumed.data, author=current_user)
            db.session.add(day)
        newExercise = exerciseTable(author=current_user, day=day, exerciseDuration=form.exerciseDuration.data, exerciseType=form.exerciseType.data, exerciseDistance=form.exerciseDistance.data)
        db.session.add(newExercise)        
        db.session.commit()
        return redirect(url_for("daily_form"))
    return render_template("daily_exercise.html", user=current_user, form=form)

@app.route("/daily_task", methods=["GET", "POST"])
@login_required
def daily_task():
    form = newTaskForm()
    return render_template("daily_task.html", user=current_user, form=form)

@app.route("/daily")
@login_required
def daily():
    return render_template("daily.html", user=current_user)

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
        flash(f"You are logged in as {current_user.username}")
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

@app.route("/ideas", methods=["GET", "POST"])
def ideas():
    form = ideasForm()
    ideas = ideaTable.query.all()
    if form.validate_on_submit():
        ideaNote = form.ideaNote.data
        idea = ideaTable(note=ideaNote)
        db.session.add(idea)
        db.session.commit()
        ideas = ideaTable.query.all()
        return render_template("ideas.html", form=form, ideas=ideas, user=current_user)    
    return render_template("ideas.html", form=form, ideas=ideas, user=current_user)

@app.route("/edit_idea<int:id>", methods=["GET", "POST"])
def edit_idea(id):
    idea = ideaTable.query.get_or_404(id)
    form = ideasForm()
    form.ideaNote.data = idea.note
    ideas = None
    if form.validate_on_submit():
        idea.note = form.ideaNote.data
        db.session.commit()
        return redirect(url_for("ideas"))
    return render_template("ideas.html", form=form, ideas=ideas, user=current_user)    

@app.route("/delete_idea/<int:id>")
def delete_idea(id):
    idea = ideaTable.query.get_or_404(id)
    db.session.delete(idea)
    db.session.commit()
    flash("Task successfully deleted")
    return redirect(url_for("ideas"))
    
@app.route("/edit_profile/<int:id>", methods=["GET", "POST"])
@login_required
def edit_profile(id):
    form = editProfileForm()
    if current_user.id != id:
        flash("You are not authorized to make changes to that account")
        return redirect(url_for("home"))
    if request.method == "GET":
        return render_template("register.html", form=form, user=current_user)
    elif form.validate_on_submit():
        if current_user.check_password(form.password_check.data):
            current_user.set_password(form.password.data)
            db.session.commit()
            flash("Your password has been updated")
            return redirect(url_for("home"))
        else:
            flash("Incorrect password validation")
            return render_template("register.html", form=form, user=current_user)
    else:
        flash("Incorrect password validation")
        return render_template("register.html", form=form, user=current_user)

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
    return render_template("new_task.html", form=form, user=current_user)

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
        return render_template("new_task.html", form=form, user=current_user)

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
    return render_template("new_content.html", form=form, user=current_user)

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
        return render_template("new_content.html", form=form, user=current_user)

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
    return render_template("new_news.html", form=form, user=current_user)

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
        return render_template("new_news.html", form=form, user=current_user)

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

#### Events ####
@app.route("/new_event", methods=["POST", "GET"])
@login_required
def new_event():
    form = newEventForm()
    if form.validate_on_submit():
        newEvent = eventTable(eventType=form.eventType.data, 
                              eventDatetime=form.eventDatetime.data, 
                              eventLocation=form.eventLocation.data, 
                              eventNote=form.eventNote.data, 
                              author=current_user)
        exerciseEvent = exerciseTable(exerciseDuration=form.exerciseDuration.data,
                                      exerciseType=form.exerciseType.data,
                                      exerciseDistance=form.exerciseDistance.data,
                                      event=newEvent,
                                      author=current_user)
        db.session.add(newEvent)
        db.session.add(exerciseEvent)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("new_event.html", form=form, user=current_user)

@app.route("/update_event/<int:id>", methods=["POST", "GET"])
@login_required
def update_event(id):
    event = eventTable.query.get_or_404(id)
    if event.author != current_user:
        flash("You are not authorized to update this item")
        return redirect(url_for("home"))
    form = newEventForm()
    if form.validate_on_submit():
        event.eventType=form.eventType.data
        event.eventDatetime=form.eventDatetime.data
        event.eventLocation=form.eventLocation.data
        event.eventNote=form.eventNote.data

        exercise = event.exercises.first()
        exercise.exerciseDuration=form.exerciseDuration.data
        exercise.exerciseType=form.exerciseType.data
        exercise.exerciseDistance=form.exerciseDistance.data

        db.session.commit()
        flash("Your news item has been updated")
        return redirect(url_for("home"))
    elif request.method == "GET":
        form.eventType.data = event.eventType
        form.eventDatetime.data = event.eventDatetime
        form.eventLocation.data = event.eventLocation
        form.eventNote.data = event.eventNote

        exercise = event.exercises.first()
        if event.exercises:
            form.exerciseDuration.data = exercise.exerciseDuration
            form.exerciseType.data = exercise.exerciseType
            form.exerciseDistance.data = exercise.exerciseDistance
        return render_template("new_event.html", form=form, user=current_user)

@app.route("/delete_event/<int:id>")
@login_required
def delete_event(id):
    event = eventTable.query.get_or_404(id)
    if event.author == current_user:
        db.session.delete(event)
        db.session.commit()
        flash("Event successfully deleted")
        return redirect(url_for("home"))
    else:
        flash("User not authorized to delete")
        return redirect(url_for("home"))

# About Page
@app.route("/about")
@login_required
def about():
    return render_template("about.html", user=current_user)