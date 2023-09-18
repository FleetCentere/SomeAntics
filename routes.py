from flask import Flask, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import desc
from datetime import datetime, date, timedelta
from werkzeug.urls import url_parse
from ProjectFiles import app, db
from ProjectFiles.secFinancials import finSearch
from ProjectFiles.holderSearch import holderSearch
from ProjectFiles.forms import loginForm, RegistrationForm, editProfileForm, newTaskForm, newContentForm, newNewsForm, newEventForm, ideasForm, dailyForm, newExerciseForm, sourcesForm
from ProjectFiles.models import userTable, dayTable, taskTable, newsTable, eventTable, contentTable, exerciseTable, personsTable, ideaTable, sourcesTable
from ProjectFiles.stockPrice import sp500

@app.route("/", defaults={"day_id": None}, methods=["GET", "POST"])
@app.route("/daily_form", defaults={"day_id": None}, methods=["GET", "POST"])
@app.route("/daily_form/<int:day_id>", methods=["GET", "POST"])
@login_required
def daily_form(day_id):
    n = 20
    time = datetime.now()
    today = time.date()
    latest_date = today - timedelta(days=n)
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
    parts = displayDay.split("/")
    parts[2] = parts[2][2:]
    displayDay = "/".join(parts)
    sp = sp500()
    if form.validate_on_submit():
        date = form.date.data
        weight = form.weight.data
        sleep = form.sleep.data
        morning = form.morning.data
        afternoon = form.afternoon.data
        evening = form.evening.data
        journal = form.journal.data
        todayEntry = dayTable.query.filter_by(date=date, user_id=current_user.id).first()
        if todayEntry == None:
            newEntry = dayTable(date=date, 
                                weight=weight, 
                                sleep=sleep, 
                                morning=morning, 
                                afternoon=afternoon, 
                                evening=evening, 
                                journal=journal, 
                                author=current_user)
            db.session.add(newEntry)
            db.session.commit()
            flash("Your daily items have been submitted")
            return redirect(url_for("daily_form"))
        else:
            todayEntry.weight = form.weight.data
            todayEntry.sleep = form.sleep.data
            todayEntry.morning = form.morning.data
            todayEntry.afternoon = form.afternoon.data
            todayEntry.evening = form.evening.data
            todayEntry.journal = form.journal.data
            flash("Your daily items have been updated")
            db.session.commit()
            return redirect(url_for("daily_form", day_id = todayEntry.id))
        return redirect(url_for("daily_form"))
    elif request.method == "GET":
        if day_id is not None:
            dayEntry = dayTable.query.filter_by(id = day_id).first()
            form.date.data = dayEntry.date
            form.weight.data = dayEntry.weight
            form.sleep.data = dayEntry.sleep
            form.morning.data = dayEntry.morning
            form.afternoon.data = dayEntry.afternoon
            form.evening.data = dayEntry.evening
            form.journal.data = dayEntry.journal
        elif day_id is None:
            todayEntry = dayTable.query.filter_by(date=today, user_id=current_user.id).first()
            if todayEntry != None:
                form.date.data = todayEntry.date
                form.weight.data = todayEntry.weight
                form.sleep.data = todayEntry.sleep
                form.morning.data = todayEntry.morning
                form.afternoon.data = todayEntry.afternoon
                form.evening.data = todayEntry.evening
                form.journal.data = todayEntry.journal
        return render_template("daily_form.html", 
                                    counts_dict=counts_dict, 
                                    days=days, 
                                    user=current_user, 
                                    form=form, 
                                    displayTime=displayTime, 
                                    displayDay=displayDay, 
                                    sp=sp,
                                    today_date=today)
    else:
        return redirect(url_for("daily_form"))

### content ###
@app.route("/daily_content", methods=["GET", "POST"])
@login_required
def daily_content():
    total_days = 10
    latest_date = datetime.now() - timedelta(days=total_days)
    days = db.session.query(dayTable).filter(dayTable.date >= latest_date)
    days = days.order_by(desc(dayTable.date)).all()
    form = newContentForm()
    category_tuple = db.session.query(contentTable.contentType).distinct().all()
    categories = [category[0] for category in category_tuple]
    content_dict = {}
    for day in days:
        content_dict[day.date] = {}
        for category in categories:
            content_dict[day.date][category] = contentTable.query.filter(contentTable.day == day, 
                                                                         contentTable.contentType == category, 
                                                                         contentTable.user_id == current_user.id).count()
    contents = contentTable.query.filter(contentTable.user_id == current_user.id)
    contents = contents.order_by(desc(contentTable.dateConsumed)).all()
    if form.validate_on_submit():
        day = dayTable.query.filter_by(date=form.dateConsumed.data, author=current_user).first()
        if day == None:
            day = dayTable(date=form.dateConsumed.data, author=current_user)
            db.session.add(day)
        newContent = contentTable(dateConsumed=form.dateConsumed.data, 
                                  dateMade=form.dateMade.data, 
                                  contentType=form.contentType.data, 
                                  contentCreator=form.contentCreator.data, 
                                  contentLink=form.contentLink.data, 
                                  contentRating=form.contentRating.data, 
                                  contentSubject=form.contentSubject.data, 
                                  contentNote=form.contentNote.data, 
                                  contentComplete = form.contentComplete.data, 
                                  author=current_user, 
                                  day=day)
        db.session.add(newContent)
        db.session.commit()
        flash("Your content has been added")
        return redirect(url_for("daily_content"))
    return render_template("daily_content.html", 
                            user=current_user, 
                            form=form, 
                            content_dict=content_dict, 
                            categories=categories, 
                            contents=contents)

@app.route("/content_edit/<int:id>", methods=["GET", "POST"])
@login_required
def content_edit(id):
    form = newContentForm()
    contentEntry = contentTable.query.filter_by(id = id).first()
    if form.validate_on_submit():
        contentEntry.contentComplete = form.contentComplete.data
        contentEntry.dateConsumed = form.dateConsumed.data
        contentEntry.dateMade = form.dateMade.data
        contentEntry.contentType = form.contentType.data
        contentEntry.contentCreator = form.contentCreator.data
        contentEntry.contentLink = form.contentLink.data
        contentEntry.contentRating = form.contentRating.data
        contentEntry.contentSubject = form.contentSubject.data
        contentEntry.contentNote = form.contentNote.data
        day = dayTable.query.filter_by(date=contentEntry.dateConsumed).first()
        if day is not None:
            contentEntry.day_id = day.id
        db.session.commit()
        flash("Your content has been updated")
        return redirect(url_for("daily_content"))
    if request.method == "GET":
        form.contentComplete.data = contentEntry.contentComplete
        form.dateConsumed.data = contentEntry.dateConsumed
        form.dateMade.data = contentEntry.dateMade
        form.contentType.data = contentEntry.contentType
        form.contentCreator.data = contentEntry.contentCreator
        form.contentLink.data = contentEntry.contentLink
        form.contentRating.data = contentEntry.contentRating
        form.contentSubject.data = contentEntry.contentSubject
        form.contentNote.data = contentEntry.contentNote
    return render_template("content_edit.html", user=current_user, form=form)

@app.route("/delete_daily_content/<int:id>")
@login_required
def delete_daily_content(id):
    content = contentTable.query.get_or_404(id)
    if content.author == current_user:
        db.session.delete(content)
        db.session.commit()
        flash("Content item successfully deleted")
        return redirect(url_for("daily_content"))
    else:
        flash("User not authorized to delete")
        return redirect(url_for("daily_content"))  

### exercise ###
@app.route("/daily_exercise/", defaults={"id": None}, methods=["GET", "POST"])
@app.route("/daily_exercise/<int:id>", methods=["GET", "POST"])
@login_required
def daily_exercise(id):
    form = newExerciseForm()
    if form.validate_on_submit():
        if id is None:
            day = dayTable.query.filter_by(date=form.exerciseDate.data).first()
            if day == None:
                day = dayTable(date=form.exerciseDate.data, author=current_user)
                db.session.add(day)
            newExercise = exerciseTable(author=current_user, 
                                        day=day, 
                                        exerciseDuration=form.exerciseDuration.data, 
                                        exerciseType=form.exerciseType.data, 
                                        exerciseDistance=form.exerciseDistance.data)
            db.session.add(newExercise)        
            db.session.commit()
            return redirect(url_for("daily_exercise"))
        elif id is not None:
            exercise = exerciseTable.query.get_or_404(id)
            exercise.exerciseType = form.exerciseType.data
            exercise.exerciseDuration = form.exerciseDuration.data
            exercise.exerciseDistance = form.exerciseDistance.data
            day = dayTable.query.filter(dayTable.date == form.exerciseData.data).filter(dayTable.author == current_user).first()
            exercise.day = day
            db.session.commit()
            return redirect(url_for("daily_exercise"))
    if request.method == "GET":
        if id is not None:
            exercise = exerciseTable.query.get_or_404(id)
            form.exerciseType.data = exercise.exerciseType
            form.exerciseDuration.data = exercise.exerciseDuration
            form.exerciseDistance.data = exercise.exerciseDistance
            day = dayTable.query.filter_by(id = exercise.day_id).first()
            try:
                form.exerciseDate.data = day.date
            except:
                form.exerciseDate.data = None
    exercises = exerciseTable.query.filter(exerciseTable.author == current_user)
    exercises = exercises.join(dayTable).order_by(desc(dayTable.date)).all()
    return render_template("daily_exercise.html", 
                            user=current_user, 
                            form=form, 
                            exercises=exercises)

@app.route("/delete_daily_exercise/<int:id>")
@login_required
def delete_daily_exercise(id):
    exercise = exerciseTable.query.get_or_404(id)
    if exercise.author == current_user:
        db.session.delete(exercise)
        db.session.commit()
        flash("Exercise item successfully deleted")
        return redirect(url_for("daily_exercise"))
    else:
        flash("User not authorized to delete")
        return redirect(url_for("daily_exercise"))    

### task ###
@app.route("/daily_task/", defaults={"task_id": None}, methods=["GET", "POST"])
@app.route("/daily_task/<int:task_id>", methods=["GET", "POST"])
@login_required
def daily_task(task_id):
    form = newTaskForm()
    tasks = taskTable.query.order_by(desc(taskTable.dateEntered)).all()
    if task_id is not None:
        task = taskTable.query.filter_by(id=task_id).first()
        form.taskCategory.data = task.taskCategory
        form.taskName.data = task.taskName
        form.taskNote.data = task.taskNote
        form.taskLink.data = task.taskLink
    if form.validate_on_submit():
        if task_id == None:
            newTask = taskTable(author=current_user, 
                                taskCategory=form.taskCategory.data, 
                                taskName=form.taskName.data, 
                                taskLink=form.taskLink.data, 
                                taskNote=form.taskNote.data)
            db.session.add(newTask)
        else:
            task.taskCategory = form.taskCategory.data
            task.taskName = form.taskName.data
            task.taskNote = form.taskNote
            task.taskLink = form.taskLink
        db.session.commit()
        return redirect(url_for("daily_task"))
    return render_template("daily_task.html", 
                            user=current_user, 
                            form=form, 
                            tasks=tasks)

@app.route("/delete_task/<int:task_id>")
@login_required
def delete_task(task_id):
    task = taskTable.query.get_or_404(task_id)
    if task.author == current_user:
        db.session.delete(task)    
        db.session.commit()
        flash("Task successfully deleted")
        return redirect(url_for("daily_task"))
    else:
        flash("User not authorized to delete")
        return redirect(url_for("daily_events"))

### events ###
@app.route("/daily_events/", defaults={"id": None}, methods=["GET", "POST"])
@app.route("/daily_events/<int:id>", methods=["GET", "POST"])
def daily_events(id):
    print(f"id is {id}")
    form = newEventForm()
    events = eventTable.query.filter_by(author=current_user)
    events = events.join(dayTable).order_by(desc(dayTable.date)).all()
    if id is not None:
        event = eventTable.query.get_or_404(id)
    if form.validate_on_submit():
        eventType = form.eventType.data
        eventLocation = form.eventLocation.data
        eventNote = form.eventNote.data
        eventDate = form.eventDate.data
        eventTime = form.eventTime.data
        day = dayTable.query.filter(dayTable.date == eventDate).filter(dayTable.author == current_user).first()
        if id is None:
            eventEntry = eventTable(author=current_user, 
                           eventType=eventType, 
                           eventLocation=eventLocation, 
                           eventNote=eventNote,
                           eventTime=eventTime,
                           day=day)
            db.session.add(eventEntry)
            db.session.commit()
            return redirect(url_for("daily_events"))
        elif id is not None:
            event.eventType = form.eventType.data
            event.eventLocation = form.eventLocation.data
            event.eventTime = form.eventTime.data
            event.eventNote = form.eventNote.data
            day = dayTable.query.filter(dayTable.date == form.eventDate.data).filter(dayTable.author == current_user).first()
            event.day = day
            db.session.commit()
            return redirect(url_for("daily_events"))
    else:
        print(form.errors)
    if request.method == "GET":
        print("method is get")
        if id is not None:
            form.eventType.data = event.eventType
            form.eventLocation.data = event.eventLocation
            form.eventNote.data = event.eventNote
            day = dayTable.query.filter_by(id = event.day_id).first()
            try:
                form.eventDate.data = day.date
            except:
                form.eventDate.data = None
            form.eventTime.data = event.eventTime
    elif request.method == "POST":
        print("method is post")
    return render_template("daily_event.html", 
                            user=current_user,
                            form=form,
                            events=events)

@app.route("/delete_daily_event/<int:id>")
@login_required
def delete_daily_event(id):
    event = eventTable.query.get_or_404(id)
    if event.author == current_user:
        db.session.delete(event)    
        db.session.commit()
        flash("Event item successfully deleted")
        return redirect(url_for("daily_events"))
    else:
        flash("User not authorized to delete")
        return redirect(url_for("daily_events"))

### news ###
@app.route("/daily_news", defaults={"news_id": None}, methods=["GET", "POST"])
@app.route("/daily_news/<int:news_id>", methods=["GET", "POST"])
@login_required
def daily_news(news_id):
    form = newNewsForm()
    news = newsTable.query.filter_by(user_id = current_user.id).all()
    if form.validate_on_submit():
        if news_id is None:
            newsType = form.newsType.data
            newsTitle = form.newsTitle.data
            newsNote = form.newsNote.data
            newsLink = form.newsLink.data
            newsTicker = form.newsTicker.data
            newsDatePosted = form.newsDatePosted.data
            day = dayTable.query.filter_by(user_id=current_user.id, date=newsDatePosted).first()
            news = newsTable(newsType=newsType, 
                             newsTitle=newsTitle, 
                             newsNote=newsNote, 
                             newsLink=newsLink, 
                             newsTicker=newsTicker, 
                             author=current_user,
                             day=day)
            db.session.add(news)
            db.session.commit()
            flash("Your news item has been added")
            return redirect(url_for("daily_news"))
        if news_id is not None:
            news = newsTable.query.get_or_404(news_id)
            news.newsType = form.newsType.data
            news.newsTitle = form.newsTitle.data
            news.newsNote = form.newsNote.data
            news.newsLink = form.newsLink.data
            news.newsTicker = form.newsTicker.data
            db.session.commit()
            flash("Your news item has been updated")
            return redirect(url_for("daily_news"))
    if request.method == "GET":
        if news_id is not None:
            newsItem = newsTable.query.get_or_404(news_id)
            day = dayTable.query.filter_by(id = newsItem.day_id).first()
            if day is not None:
                form.newsDatePosted.data = day.date
            form.newsType.data = newsItem.newsType
            form.newsTitle.data = newsItem.newsTitle
            form.newsNote.data = newsItem.newsNote
            form.newsLink.data = newsItem.newsLink
            form.newsTicker.data = newsItem.newsTicker
    return render_template("daily_news.html", user=current_user, news=news, form=form)

@app.route("/delete_news/<int:news_id>")
@login_required
def delete_news(news_id):
    news = newsTable.query.get_or_404(news_id)
    db.session.delete(news)
    db.session.commit()
    flash("Event item successfully deleted")
    return redirect(url_for("daily_news"))

### webpage ideas ###
@app.route("/webpage_ideas", defaults={"id": None}, methods=["GET", "POST"])
@app.route("/webpage_ideas/<int:id>", methods=["GET", "POST"])
@login_required
def webpage_ideas(id):
    form = ideasForm()
    sForm = sourcesForm()
    ideas = ideaTable.query.all()
    sources = sourcesTable.query.all()
    if form.validate_on_submit():
        if id is None:
            ideaNote = form.ideaNote.data
            idea = ideaTable(note=ideaNote)
            db.session.add(idea)
            db.session.commit()
            return redirect(url_for("webpage_ideas"))
        elif id is not None:
            idea = ideaTable.query.get_or_404(id)
            idea.note = form.ideaNote.data
            db.session.commit()
            return redirect(url_for("webpage_ideas"))
    if sForm.validate_on_submit():
        sourceTopic = sForm.sourceTopic.data
        sourceLink = sForm.sourceLink.data
        sourceNote = sForm.sourceNote.data
        source = sourcesTable(sourceTopic=sourceTopic, sourceLink=sourceLink, sourceNote=sourceNote)
        db.session.add(source)
        db.session.commit()
        return redirect(url_for("webpage_ideas"))
    if request.method == "GET":
        if id is not None:
            idea = ideaTable.query.get_or_404(id)
            form.ideaNote.data = idea.note
    return render_template("webpage_ideas.html",
                            form=form,
                            sForm=sForm,
                            ideas=ideas, 
                            sources=sources,
                            user=current_user)

@app.route("/delete_webpage_idea/<int:id>")
@login_required
def delete_webpage_idea(id):
    idea = ideaTable.query.get_or_404(id)
    db.session.delete(idea)
    db.session.commit()
    flash("Event item successfully deleted")
    return redirect(url_for("webpage_ideas"))

@app.route("/daily")
@login_required
def daily():
    return render_template("daily.html", user=current_user)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("daily_form"))
    form = loginForm()
    if form.validate_on_submit():
        user = userTable.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("daily_form")
        flash(f"You are logged in as {current_user.username}")
        return redirect(next_page)
    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("daily_form"))
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

@app.route("/edit_profile/<int:id>", methods=["GET", "POST"])
@login_required
def edit_profile(id):
    form = editProfileForm()
    if current_user.id != id:
        flash("You are not authorized to make changes to that account")
        return redirect(url_for("daily_form"))
    if request.method == "GET":
        return render_template("register.html", form=form, user=current_user)
    elif form.validate_on_submit():
        if current_user.check_password(form.password_check.data):
            current_user.set_password(form.password.data)
            db.session.commit()
            flash("Your password has been updated")
            return redirect(url_for("daily_form"))
        else:
            flash("Incorrect password validation")
            return render_template("register.html", form=form, user=current_user)
    else:
        flash("Incorrect password validation")
        return render_template("register.html", form=form, user=current_user)

# About Page
@app.route("/about")
@login_required
def about():
    return render_template("about.html", user=current_user)