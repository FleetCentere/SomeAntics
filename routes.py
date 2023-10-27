from flask import Flask, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import desc
from datetime import datetime, date, timedelta
from werkzeug.urls import url_parse
from ProjectFiles import app, db
from ProjectFiles.secFinancials import finSearch
from ProjectFiles.holderSearch import holderSearch
from ProjectFiles.forms import loginForm, RegistrationForm, editProfileForm, newTaskForm, newContentForm, newNewsForm, newEventForm, ideasForm, dailyForm, newExerciseForm, sourcesForm, companyForm, personForm, listForm, computerScienceForm, computerSciencePosts, jobForm
from ProjectFiles.models import userTable, dayTable, taskTable, newsTable, eventTable, contentTable, exerciseTable, personsTable, ideaTable, sourcesTable, companyTable, csTable, csPosts, jobTable
from ProjectFiles.stockPrice import sp500
from ProjectFiles.cusipLookup import cusipLookup
from ProjectFiles.newsRun import newsRun
from ProjectFiles.companyInfo import getInfo, getRandomTicker

@app.route("/")
@app.route("/home")
@login_required
def home():
    try:
        articles = newsRun()
    except:
        articles = {}
    current = datetime.now()
    displayTime = current.strftime("%I:%M %p")
    if displayTime.startswith("0"):
        displayTime = displayTime[1:]
    displayDay = f"{current.strftime('%A')[:3]} {current.month}/{current.day}/{current.year}"
    parts = displayDay.split("/")
    parts[2] = parts[2][2:]
    displayDay = "/".join(parts)
    prices = sp500()
    dayDelta = 14
    current = datetime.now().date()
    latest_date = current - timedelta(days=dayDelta)
    days = db.session.query(dayTable).filter(dayTable.date >= latest_date, dayTable.user_id == current_user.id)
    days = days.order_by(desc(dayTable.date)).all()
    n = 5
    events = eventTable.query.filter(current_user.id == eventTable.user_id)
    events = events.join(dayTable).order_by(desc(dayTable.date)).limit(n).all()
    cs = csTable.query.filter(current_user.id == csTable.user_id)
    cs = cs.order_by(desc(csTable.dateAdded)).all()
    exercises = exerciseTable.query.filter(current_user.id == exerciseTable.user_id)
    exercises = exercises.join(dayTable).order_by(desc(dayTable.date)).limit(n).all()
    tasks = taskTable.query.filter(current_user.id == taskTable.user_id)
    tasks = tasks.order_by(desc(taskTable.dateEntered)).all()
    contents = contentTable.query.filter(current_user.id == contentTable.user_id)
    contents = contents.join(dayTable).order_by(desc(dayTable.date)).limit(n).all()
    try:
        t_minus_1 = (prices[2]/prices[1])-1
        t_minus_2 = (prices[2]/prices[0])-1
        sp = [f"{prices[0]:.2f}", f"{t_minus_1*100:.2f}", f"{t_minus_2:2f}"]
    except:
        sp = ["na", "na", "na"]
    return render_template("home.html", 
                            user=current_user,
                            cs=cs,
                            tasks=tasks,
                            events=events,
                            exercises=exercises,
                            displayTime=displayTime, 
                            displayDay=displayDay,
                            sp=sp,
                            articles=articles,
                            days=days,
                            contents=contents)

@app.route("/cards/<string:category>", methods=["GET", "POST"])
@login_required
def cards(category):
    n = 20
    items = [] # items will hold a list of dictionaries with each ith element of items one dictionary per relevant item of set
    if category == "Content":
        form = newContentForm()
        contents = contentTable.query.filter_by(user_id=current_user.id).join(dayTable).order_by(desc(dayTable.date)).limit(n)
        headers = ["Date", "Type", "Creator", "Subject"]
        items.append(headers)
        for i, content in enumerate(contents):
            dictionary = {"id": content.id, 
                          "day": content.day, 
                          "type": content.contentType, 
                          "name": content.contentCreator, 
                          "subject": content.contentSubject}
            items.append(dictionary) 
    elif category == "Exercise":
        form = newExerciseForm()
        exercises = exerciseTable.query.filter_by(user_id=current_user.id).join(dayTable).order_by(desc(dayTable.date)).limit(n)
        headers = ["Date", "Type", "Distance", "Time"]
        items.append(headers)
        for i, exercise in enumerate(exercises):
            dictionary = {"id": exercise.id, 
                          "day": exercise.day, 
                          "type": exercise.exerciseType, 
                          "distance": exercise.exerciseDistance, 
                          "duration": exercise.exerciseDuration}
            items.append(dictionary)
    return render_template("cards.html", 
                            user=current_user, 
                            items=items,
                            category=category,
                            form=form)

@app.route("/computerScience/", defaults={"cat_id": None}, methods=["GET", "POST"])
@app.route("/computerScience/<int:cat_id>", methods=["GET", "POST"])
@login_required
def computerScience(cat_id):
    form = computerScienceForm()
    cs = csTable.query.filter_by(user_id=current_user.id).all()
    if form.validate_on_submit():
        name = form.name.data
        category = form.category.data
        link = form.link.data
        if cat_id is None:
            cs = csTable(user_id=current_user.id, name=name, category=category, link=form.link.data, dateAdded=datetime.now().date())
            db.session.add(cs)
            db.session.commit()
            flash("Your category has been added")
            return redirect(url_for("computerScience"))
        else:
            cat = csTable.query.get_or_404(cat_id)
            cat.name = name
            cat.category = category
            cat.link = link
            db.session.commit()
            flash("Your category has been updated")
            return redirect(url_for("computerScience"))
    if cat_id is not None:
        cat = csTable.query.get_or_404(cat_id)
        form.name.data = cat.name
        form.category.data = cat.category
        form.link.data = cat.link
    return render_template("computerScience.html",
                            form=form, 
                            cs=cs,
                            user=current_user)

@app.route("/computerScienceCat/<int:cat_id>", defaults={"post_id": None}, methods=["GET", "POST"])
@app.route("/computerScienceCat/<int:cat_id>/<int:post_id>", methods=["GET", "POST"])
@login_required
def computerScienceCat(cat_id, post_id):
    cs = csTable.query.get_or_404(cat_id)
    if post_id is not None:
        post = csPosts.query.get_or_404(post_id)
    items = cs.posts
    form = computerSciencePosts()
    if request.method == "GET":   
        if post_id is not None:
            post = csPosts.query.get_or_404(post_id)
            form.note.data = post.note
            form.title.data = post.title
        return render_template("computerScienceCat.html",
                            cs=cs,
                            form=form,
                            items=items,
                            user=current_user)
    if form.validate_on_submit():
        if post_id is None:
            csPost = csPosts(cs_id=cs.id, user_id=current_user.id, note=form.note.data, title=form.title.data, dateAdded=datetime.now().date())
            db.session.add(csPost)
            db.session.commit()
            items = cs.posts
            return redirect(url_for("computerScienceCat", cat_id=cs.id))
        elif post_id is not None:
            post = csPosts.query.get_or_404(post_id)
            post.note = form.note.data
            post.title = form.title.data
            db.session.commit()
            return redirect(url_for("computerScienceCat", cat_id=cs.id))

@app.route("/deleteComputerScience/<int:cat_id>", methods=["POST", "GET"])
@login_required
def deleteComputerScience(cat_id):
    cs = csTable.query.get_or_404(cat_id)
    if cs.user_id != current_user.id:
        flash("You are not authorized to delete this item")
        return redirect(url_for("computerScience"))
    db.session.delete(cs)
    db.session.commit()
    flash("The item has been deleted")
    return redirect(url_for("computerScience"))

@app.route("/deleteComputerScienceCat/<int:post_id>", methods=["POST", "GET"])
@login_required
def deleteComputerScienceCat(post_id):
    post = csPosts.query.get_or_404(post_id)
    cat = csTable.query.get_or_404(post.cs_id)
    if post.user_id != current_user.id:
        flash("You are not authorized to delete this item")
        return redirect(url_for("computerScienceCat", cat_id=cat.id))
    db.session.delete(post)
    db.session.commit()
    flash("The post has been deleted")
    return redirect(url_for("computerScienceCat", cat_id=cat.id))

@app.route("/jobs", defaults={"job_id": None}, methods=["GET", "POST"])
@app.route("/jobs/<int:job_id>", methods=["GET", "POST"])
@login_required
def jobs(job_id):
    form = jobForm()
    jobs = jobTable.query.filter_by(user_id=current_user.id).all()
    if form.validate_on_submit():
        if job_id is None:
            newJob = jobTable(user_id=current_user.id, job=form.job.data, status=form.status.data, contact=form.contact.data, dateAdded=datetime.now().date())
            db.session.add(newJob)
            db.session.commit()
            flash("Your job has been added")
            return redirect(url_for('jobs'))
        else:
            job = jobTable.query.get_or_404(job_id)    
            job.job = form.job.data
            job.status = form.status.data
            job.contact = form.contact.data
            job.dateUpdated = dateAdded=datetime.now().date()
            db.session.commit()
            flash("Your job has been updated")
            return redirect(url_for('jobs'))
    if job_id is not None:
        job = jobTable.query.get_or_404(job_id)
        if job.user_id != current_user.id:
            flash("You are not authorized to edit that entry")
            return redirect("jobs")
        form.job.data = job.job
        form.status.data = job.status
        form.contact.data = job.contact
    return render_template("jobs.html", 
                            form=form,
                            jobs=jobs,
                            user=current_user)

@app.route("/NHLConnections", methods=["GET", "POST"])
@login_required
def NHLConnections():
    return render_template("NHLConnections.html",
                            user=current_user)

@app.route("/daily_form", defaults={"day_id": None}, methods=["GET", "POST"])
@app.route("/daily_form/<int:day_id>", methods=["GET", "POST"])
@login_required
def daily_form(day_id):
    n = 20
    current = datetime.now()
    today = datetime.now().date()
    latest_date = today - timedelta(days=n)
    days = db.session.query(dayTable).filter(dayTable.date >= latest_date, dayTable.user_id == current_user.id)
    days = days.order_by(desc(dayTable.date)).all()
    counts_dict = {}
    for day in days:
        counts_dict[day] = {"exercise": db.session.query(exerciseTable).filter(exerciseTable.day_id == day.id).filter(exerciseTable.user_id == current_user.id).count(),
                            "contents": db.session.query(contentTable).filter(contentTable.day_id == day.id).filter(contentTable.user_id == current_user.id).count(),
                            "events": db.session.query(eventTable).filter(eventTable.day_id == day.id).filter(eventTable.user_id == current_user.id).count(),
                            "news": db.session.query(newsTable).filter(newsTable.day_id == day.id).filter(newsTable.user_id == current_user.id).count()}
    form = dailyForm()
    displayTime = current.strftime("%I:%M %p")
    if displayTime.startswith("0"):
        displayTime = displayTime[1:]
    displayDay = f"{current.strftime('%A')[:3]} {current.month}/{current.day}/{current.year}"
    parts = displayDay.split("/")
    parts[2] = parts[2][2:]
    displayDay = "/".join(parts)
    prices = sp500()
    try:
        t_minus_1 = (prices[2]/prices[1])-1
        t_minus_2 = (prices[2]/prices[0])-1
        sp = [f"{prices[0]:.2f}", f"{t_minus_1*100:.2f}", f"{t_minus_2:2f}"]
    except:
        sp = ["na", "na", "na"]
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
@app.route("/daily_content", defaults={"content_id": None}, methods=["GET", "POST"])
@app.route("/daily_content/<int:content_id>", methods=["GET", "POST"])
@login_required
def daily_content(content_id):
    total_days = 10
    n = 20
    latest_date = datetime.now() - timedelta(days=total_days)
    days = db.session.query(dayTable).filter(dayTable.date >= latest_date, dayTable.user_id == current_user.id)
    days = days.order_by(desc(dayTable.date)).all()
    form = newContentForm()
    category_tuple = db.session.query(contentTable.contentType).distinct().all()
    categories = [category[0] for category in category_tuple]
    form.contentType.choices = [("", "Select a Type")] + sorted([(category, category) for category in categories])
    content_dict = {}
    for day in days:
        content_dict[day.date] = {}
        for category in categories:
            content_dict[day.date][category] = contentTable.query.filter(contentTable.day == day, 
                                                                         contentTable.contentType == category, 
                                                                         contentTable.user_id == current_user.id).count()
    contents = contentTable.query.filter(contentTable.user_id == current_user.id)
    contents = contents.order_by(desc(contentTable.dateConsumed)).limit(n).all()
    if form.validate_on_submit():
        if content_id is None:
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
        else:
            contentEntry = contentTable.query.get_or_404(content_id)
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
        if content_id is not None:
            contentEntry = contentTable.query.get_or_404(content_id)
            if contentEntry.author == current_user:
                form.contentComplete.data = contentEntry.contentComplete
                form.dateConsumed.data = contentEntry.dateConsumed
                form.dateMade.data = contentEntry.dateMade
                form.contentType.data = contentEntry.contentType
                form.contentCreator.data = contentEntry.contentCreator
                form.contentLink.data = contentEntry.contentLink
                form.contentRating.data = contentEntry.contentRating
                form.contentSubject.data = contentEntry.contentSubject
                form.contentNote.data = contentEntry.contentNote
            else:
                flash("User not authorized to update this content item")
    return render_template("daily_content.html", 
                            user=current_user, 
                            form=form, 
                            content_dict=content_dict, 
                            categories=categories, 
                            contents=contents)

@app.route("/delete_daily_content/<int:content_id>")
@login_required
def delete_daily_content(content_id):
    content = contentTable.query.get_or_404(content_id)
    if content.author == current_user:
        db.session.delete(content)
        db.session.commit()
        flash("Content item successfully deleted")
        return redirect(url_for("daily_content"))
    else:
        flash("User not authorized to delete")
        return redirect(url_for("daily_content"))  

### exercise ###
@app.route("/daily_exercise/", defaults={"exercise_id": None}, methods=["GET", "POST"])
@app.route("/daily_exercise/<int:exercise_id>", methods=["GET", "POST"])
@login_required
def daily_exercise(exercise_id):
    form = newExerciseForm()
    n = 10
    if form.validate_on_submit():
        if exercise_id is None:
            day = dayTable.query.filter_by(date=form.date.data).first()
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
        elif exercise_id is not None:
            exercise = exerciseTable.query.get_or_404(exercise_id)
            exercise.exerciseType = form.exerciseType.data
            exercise.exerciseDuration = form.exerciseDuration.data
            exercise.exerciseDistance = form.exerciseDistance.data
            day = dayTable.query.filter(dayTable.date == form.date.data).filter(dayTable.author == current_user).first()
            exercise.day = day
            db.session.commit()
            return redirect(url_for("daily_exercise"))
    if request.method == "GET":
        if exercise_id is not None:
            exercise = exerciseTable.query.get_or_404(exercise_id)
            form.exerciseType.data = exercise.exerciseType
            form.exerciseDuration.data = exercise.exerciseDuration
            form.exerciseDistance.data = exercise.exerciseDistance
            day = dayTable.query.filter_by(id = exercise.day_id).first()
            try:
                form.date.data = day.date
            except:
                form.date.data = None
    exercises = exerciseTable.query.filter(exerciseTable.author == current_user)
    exercises = exercises.join(dayTable).order_by(desc(dayTable.date)).limit(n).all()
    return render_template("daily_exercise.html", 
                            user=current_user, 
                            form=form, 
                            exercises=exercises)

@app.route("/delete_daily_exercise/<int:exercise_id>")
@login_required
def delete_daily_exercise(exercise_id):
    exercise = exerciseTable.query.get_or_404(exercise_id)
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
@app.route("/daily_events/", defaults={"event_id": None}, methods=["GET", "POST"])
@app.route("/daily_events/<int:event_id>", methods=["GET", "POST"])
def daily_events(event_id):
    form = newEventForm()
    n = 10
    people_choices = personsTable.query.filter_by(user_id=current_user.id)
    form.eventPeople.choices = [(person.id, person.person) for person in people_choices]
    events = eventTable.query.filter_by(author=current_user)
    events = events.join(dayTable).order_by(desc(dayTable.date)).limit(n).all()
    if event_id is not None:
        event = eventTable.query.get_or_404(event_id)
    if form.validate_on_submit():
        eventType = form.eventType.data
        eventLocation = form.eventLocation.data
        eventNote = form.eventNote.data
        eventDate = form.eventDate.data
        eventTime = form.eventTime.data
        day = dayTable.query.filter(dayTable.date == eventDate).filter(dayTable.author == current_user).first()
        if event_id is None:
            eventEntry = eventTable(author=current_user, 
                           eventType=eventType, 
                           eventLocation=eventLocation, 
                           eventNote=eventNote,
                           eventTime=eventTime,
                           day=day)
            db.session.add(eventEntry)
            db.session.commit()
            for person_id in form.eventPeople.data:
                person = personsTable.query.filter_by(id=person_id).first()
                eventEntry.attendees.append(person)
                db.session.commit()
            return redirect(url_for("daily_events"))
        elif event_id is not None:
            event.eventType = form.eventType.data
            event.eventLocation = form.eventLocation.data
            event.eventTime = form.eventTime.data
            event.eventNote = form.eventNote.data
            day = dayTable.query.filter(dayTable.date == form.eventDate.data).filter(dayTable.author == current_user).first()
            event.day = day
            db.session.commit()
            for person_id in form.eventPeople.data:
                person = personsTable.query.filter_by(id=person_id).first()
                event.attendees.append(person)
                db.session.commit()
            return redirect(url_for("daily_events"))
    else:
        print(form.errors)
    if request.method == "GET":
        if event_id is not None:
            form.eventType.data = event.eventType
            form.eventLocation.data = event.eventLocation
            form.eventNote.data = event.eventNote
            form.eventPeople.data = [(person.id, person.person) for person in event.attendees]
            day = dayTable.query.filter_by(id = event.day_id).first()
            try:
                form.eventDate.data = day.date
            except:
                form.eventDate.data = None
            form.eventTime.data = event.eventTime
    return render_template("daily_event.html", 
                            user=current_user,
                            form=form,
                            events=events)

@app.route("/delete_daily_event/<int:event_id>")
@login_required
def delete_daily_event(event_id):
    event = eventTable.query.get_or_404(event_id)
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
    news = newsTable.query.filter_by(user_id = current_user.id)
    news = news.join(dayTable).order_by(desc(dayTable.date)).all()
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
@app.route("/webpage_ideas", defaults={"webpage_id": None}, methods=["GET", "POST"])
@app.route("/webpage_ideas/<int:webpage_id>", methods=["GET", "POST"])
@login_required
def webpage_ideas(webpage_id):
    form = ideasForm()
    sForm = sourcesForm()
    ideas = ideaTable.query.all()
    sources = sourcesTable.query.all()
    if form.validate_on_submit():
        if webpage_id is None:
            ideaNote = form.ideaNote.data
            idea = ideaTable(note=ideaNote)
            db.session.add(idea)
            db.session.commit()
            return redirect(url_for("webpage_ideas"))
        elif webpage_id is not None:
            idea = ideaTable.query.get_or_404(webpage_id)
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
        if webpage_id is not None:
            idea = ideaTable.query.get_or_404(webpage_id)
            form.ideaNote.data = idea.note
    return render_template("webpage_ideas.html",
                            form=form,
                            sForm=sForm,
                            ideas=ideas, 
                            sources=sources,
                            user=current_user)

@app.route("/delete_webpage_idea/<int:webpage_id>")
@login_required
def delete_webpage_idea(webpage_id):
    idea = ideaTable.query.get_or_404(webpage_id)
    db.session.delete(idea)
    db.session.commit()
    flash("Event item successfully deleted")
    return redirect(url_for("webpage_ideas"))

### Companies
@app.route("/companies", defaults={"ticker": None}, methods=["POST", "GET"])
@app.route("/companies/<string:ticker>", methods=["POST", "GET"])
@login_required
def companies(ticker):
    form = companyForm()
    lForm = listForm()
    financials = None
    years = None
    companyInfo = None
    cusip = None
    holderTable = None
    last_row = None
    data = None
    companyList = companyTable.query.filter_by(user_id = current_user.id).all()
    companyDict = {}
    ticker = getRandomTicker()
    companyFacts = getInfo(ticker)    
    randomCUSIP = cusipLookup(ticker)
    randomInfo = {"ticker": ticker, "randomCUSIP": randomCUSIP, "companyFacts": companyFacts}
    # dictionary to store ticker, date added, market cap, 
    # share price, 1 day perf, 1 week perf, 1 year perf, date of latest SEC filing, 
    # link to latest SEC filing, link to SEC page, last earnings, next earnings
    for company in companyList:
        companyDict[company.ticker] = {}
        companyDict[company.ticker]["ticker"] = company.ticker.upper()
        companyDict[company.ticker]["Date"] = company.dateAdded
        companyDict[company.ticker]["marketCap"] = 10000
        companyData = sp500(company.ticker.upper())
        if companyData[0] == "na":
            companyDict[company.ticker]["sharePrice"] = "na"
            companyDict[company.ticker]["oneDayPerf"] = "na"
            companyDict[company.ticker]["oneWeekPerf"] = "na"
            companyDict[company.ticker]["oneYearPerf"] = "na"    
        else:
            companyDict[company.ticker]["sharePrice"] = f"{companyData[2]:.2f}"
            companyDict[company.ticker]["oneDayPerf"] = f"{(companyData[2]/companyData[1]-1)*100:.2f}"
            companyDict[company.ticker]["oneWeekPerf"] = -0.05
            companyDict[company.ticker]["oneYearPerf"] = 0.2
        companyDict[company.ticker]["lastSECFilingDate"] = datetime(2023, 8, 20)
        companyDict[company.ticker]["lastSECFilingLink"] = "https://www.espn.com"
        companyDict[company.ticker]["SECPage"] = "https://www.google.com"
        companyDict[company.ticker]["lastEarningsDate"] = datetime(2023,7,10)
        companyDict[company.ticker]["nextEarningsDate"] = datetime(2023,10,10)
    if lForm.validate_on_submit():
        ticker = lForm.ticker.data
        date = datetime.now().date()
        company = companyTable(ticker=ticker, user_id=current_user.id, dateAdded=date)
        db.session.add(company)
        db.session.commit()
        return redirect(url_for("companies"))
    if form.validate_on_submit():
        startYear = form.startYear.data
        ticker = form.ticker.data
        holderCount = form.holderCount.data
        ticker = ticker.upper()
        companyName, financials, years = finSearch(ticker, startYear)
        companyInfo = {"companyName": companyName, "ticker": ticker}
        cusip = cusipLookup(ticker)
        holderTable, last_row, CUSIP = holderSearch(ticker, holderCount)
        data = sp500(ticker)
        return render_template("companies.html", 
                            user=current_user, 
                            form=form,
                            lForm=lForm, 
                            financials=financials, 
                            years=years,
                            companyInfo=companyInfo,
                            companyDict = companyDict,
                            cusip=cusip,
                            holderTable=holderTable, 
                            last_row=last_row,
                            companyList=companyList,
                            data=data)
    return render_template("companies.html", 
                            user=current_user, 
                            form=form, 
                            lForm=lForm,
                            financials=financials, 
                            years=years,
                            companyInfo=companyInfo,
                            companyDict = companyDict,
                            cusip=cusip,
                            holderTable=holderTable, 
                            last_row=last_row,
                            companyList=companyList,
                            data=data,
                            randomInfo=randomInfo)

@app.route("/delete_company/<int:company_id>", methods=["POST", "GET"])
def delete_company(company_id):
    company = companyTable.query.get_or_404(company_id)
    if company.user_id == current_user.id:
        db.session.delete(company)
        db.session.commit()
        flash("Company has been deleted")
        return redirect(url_for("companies"))
    else:
        flash("You are not permitted to delete that company")
        return redirect(url_for("companies"))

@app.route("/people", defaults={"person_id": None}, methods=["GET", "POST"])
@app.route("/people/<int:person_id>", methods=["GET", "POST"])
def people(person_id):
    form = personForm()
    people = personsTable.query.filter_by(user_id=current_user.id).all()
    if form.validate_on_submit():
        name = form.name.data
        background = form.background.data
        birthday = form.birthday.data
        category = form.category.data
        company = form.company.data
        newPerson = personsTable(user_id=current_user.id, 
                                 person=name, 
                                 personBackground=background,
                                 personBirthday=birthday,
                                 personCategory=category,
                                 personCompany=company)
        db.session.add(newPerson)
        db.session.commit()
        return redirect(url_for("people"))
    return render_template("people.html", 
                            user=current_user, 
                            form=form,
                            people=people)

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

@app.route("/edit_profile/<int:profile_id>", methods=["GET", "POST"])
@login_required
def edit_profile(profile_id):
    form = editProfileForm()
    if current_user.id != profile_id:
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

@app.route("/playground")
def playground():
    return render_template("playground.html", user=current_user)