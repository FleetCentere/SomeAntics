# ################
# ### old code ###
# ################
# @app.route("/home_old")
# def home_old():
#     n = 8 # number of items to display in any given fieldset
#     if current_user.is_authenticated:
#         tasks = taskTable.query.filter_by(user_id=current_user.id).limit(n).all()
#         contents = contentTable.query.filter_by(user_id=current_user.id).limit(n).all()
#         newsItems = newsTable.query.filter_by(user_id=current_user.id).limit(n).all()
#         events = eventTable.query.filter_by(user_id=current_user.id).limit(n).all()
#         current = datetime.now()
#         displayTime = current.strftime("%I:%M %p")
#         displayDay = f"{current.strftime('%A')} {current.month}/{current.day}/{current.year}"
#         sp = sp500()
#         user = current_user
#         if displayTime.startswith("0"):
#             displayTime = displayTime[1:]
#         return render_template("home.html", 
#                                 user=user, 
#                                 tasks=tasks, 
#                                 contents=contents, 
#                                 newsItems=newsItems, 
#                                 events=events, 
#                                 displayTime=displayTime, 
#                                 displayDay=displayDay, 
#                                 sp=sp)
#     return redirect(url_for("login"))

# @app.route("/new_task", methods=["POST", "GET"])
# @login_required
# def new_task():
#     form = newTaskForm()
#     if form.validate_on_submit():
#         taskCategory = form.taskCategory.data
#         taskName = form.taskName.data
#         taskLink = form.taskLink.data
#         taskNote = form.taskNote.data
#         task = taskTable(taskCategory=taskCategory, 
#                          taskName=taskName, 
#                          taskLink=taskLink, 
#                          taskNote=taskNote, 
#                          author=current_user)
#         db.session.add(task)
#         db.session.commit()
#         return redirect(url_for("home_old"))
#     return render_template("new_task.html", form=form, user=current_user)

# @app.route("/update_task/<int:id>", methods=["POST", "GET"])
# @login_required
# def update_task(id):
#     task = taskTable.query.get_or_404(id)
#     if taskItem.author != current_user:
#         flask("You are not authorized to update this item")
#         return redirect(url_for("home_old"))
#     form = newTaskForm()
#     if form.validate_on_submit():
#         task.taskCategory = form.taskCategory.data
#         task.taskName = form.taskName.data
#         task.taskLink = form.taskLink.data
#         task.taskNote = form.taskNote.data
#         db.session.commit()
#         flash("Your task has been updated")
#         return redirect(url_for("home_old"))
#     elif request.method == "GET":
#         form.taskCategory.data = task.taskCategory
#         form.taskName.data = task.taskName
#         form.taskLink.data = task.taskLink
#         form.taskNote.data = task.taskNote
#         return render_template("new_task.html", form=form, user=current_user)

# @app.route("/delete_task/<int:id>")
# @login_required
# def delete_task(id):
#     task = taskTable.query.get_or_404(id)
#     if task.author == current_user:
#         db.session.delete(task)
#         db.session.commit()
#         flash("Task successfully deleted")
#         return redirect(url_for("home_old"))
#     else:
#         flash("User not authorized to delete")
#         return redirect(url_for("home_old"))

# @app.route("/new_content", methods=["POST", "GET"])
# @login_required
# def new_content():
#     form = newContentForm()
#     if form.validate_on_submit():
#         newContent = contentTable(dateMade=form.dateMade.data, 
#                                   contentType=form.contentType.data, 
#                                   contentCreator=form.contentCreator.data, 
#                                   contentLink=form.contentLink.data, 
#                                   contentRating=form.contentRating.data, 
#                                   contentSubject=form.contentSubject.data, 
#                                   contentNote=form.contentNote.data, 
#                                   author=current_user)
#         db.session.add(newContent)
#         db.session.commit()
#         return redirect(url_for("home_old"))
#     return render_template("new_content.html", form=form, user=current_user)

# @app.route("/update_content/<int:id>", methods=["POST", "GET"])
# @login_required
# def update_content(id):
#     contentItem = contentTable.query.get_or_404(id)
#     if contentItem.author != current_user:
#         flask("You are not authorized to update this item")
#         return redirect(url_for("home_old"))
#     form = newContentForm()
#     if form.validate_on_submit():
#         contentItem.dateMade = form.dateMade.data
#         contentItem.contentType = form.contentType.data
#         contentItem.contentCreator = form.contentCreator.data
#         contentItem.contentLink = form.contentLink.data
#         contentItem.contentRating = form.contentRating.data
#         contentItem.contentSubject = form.contentSubject.data
#         contentItem.contentNote = form.contentNote.data
#         db.session.commit()
#         flash("Your content has been updated")
#         return redirect(url_for("home_old"))
#     elif request.method == "GET":
#         form.dateMade.data = contentItem.dateMade
#         form.contentType.data = contentItem.contentType
#         form.contentCreator.data = contentItem.contentCreator
#         form.contentLink.data = contentItem.contentLink
#         form.contentRating.data = contentItem.contentRating
#         form.contentSubject.data = contentItem.contentSubject
#         form.contentNote.data = contentItem.contentNote
#         return render_template("new_content.html", form=form, user=current_user)

# @app.route("/delete_content/<int:id>")
# @login_required
# def delete_content(id):
#     contentItem = contentTable.query.get_or_404(id)
#     if contentItem.author == current_user:
#         db.session.delete(contentItem)
#         db.session.commit()
#         flash("Content successfully deleted")
#         return redirect(url_for("home_old"))
#     else:
#         flash("User not authorized to delete")
#         return redirect(url_for("home_old"))

# #### News ####
# @app.route("/new_news", methods=["POST", "GET"])
# @login_required
# def new_news():
#     form = newNewsForm()
#     if form.validate_on_submit():
#         newNews = newsTable(newsType=form.newsType.data, 
#                             newsTitle=form.newsTitle.data, 
#                             newsNote=form.newsNote.data, 
#                             newsLink=form.newsLink.data, 
#                             newsTicker=form.newsTicker.data, 
#                             newsDatePosted=form.newsDatePosted.data,
#                             author=current_user)
#         db.session.add(newNews)
#         db.session.commit()
#         return redirect(url_for("home_old"))
#     return render_template("new_news.html", form=form, user=current_user)

# @app.route("/update_news/<int:id>", methods=["POST", "GET"])
# @login_required
# def update_news(id):
#     newsItem = newsTable.query.get_or_404(id)
#     if newsItem.author != current_user:
#         flash("You are not authorized to update this item")
#         return redirect(url_for("home_old"))
#     form = newNewsForm()
#     if form.validate_on_submit():
#         newsItem.newsType = form.newsType.data
#         newsItem.newsTitle = form.newsTitle.data
#         newsItem.newsNote = form.newsNote.data
#         newsItem.newsLink = form.newsLink.data
#         newsItem.newsTicker = form.newsTicker.data
#         newsItem.newsDatePosted = form.newsDatePosted.data
#         db.session.commit()
#         flash("Your news item has been updated")
#         return redirect(url_for("home_old"))
#     elif request.method == "GET":
#         form.newsType.data = newsItem.newsType
#         form.newsTitle.data = newsItem.newsTitle
#         form.newsNote.data = newsItem.newsNote
#         form.newsLink.data = newsItem.newsLink
#         form.newsTicker.data = newsItem.newsTicker
#         form.newsDatePosted.data = newsItem.newsDatePosted
#         return render_template("new_news.html", form=form, user=current_user)

# @app.route("/delete_news/<int:id>")
# @login_required
# def delete_news(id):
#     newsItem = newsTable.query.get_or_404(id)
#     if newsItem.author == current_user:
#         db.session.delete(newsItem)
#         db.session.commit()
#         flash("News item successfully deleted")
#         return redirect(url_for("home"))
#     else:
#         flash("User not authorized to delete")
#         return redirect(url_for("home_old"))

# #### Events ####
# @app.route("/new_event", methods=["POST", "GET"])
# @login_required
# def new_event():
#     form = newEventForm()
#     if form.validate_on_submit():
#         newEvent = eventTable(eventType=form.eventType.data, 
#                               eventDatetime=form.eventDatetime.data, 
#                               eventLocation=form.eventLocation.data, 
#                               eventNote=form.eventNote.data, 
#                               author=current_user)
#         exerciseEvent = exerciseTable(exerciseDuration=form.exerciseDuration.data,
#                                       exerciseType=form.exerciseType.data,
#                                       exerciseDistance=form.exerciseDistance.data,
#                                       event=newEvent,
#                                       author=current_user)
#         db.session.add(newEvent)
#         db.session.add(exerciseEvent)
#         db.session.commit()
#         return redirect(url_for("home_old"))
#     return render_template("new_event.html", form=form, user=current_user)

# @app.route("/update_event/<int:id>", methods=["POST", "GET"])
# @login_required
# def update_event(id):
#     event = eventTable.query.get_or_404(id)
#     if event.author != current_user:
#         flash("You are not authorized to update this item")
#         return redirect(url_for("home_old"))
#     form = newEventForm()
#     if form.validate_on_submit():
#         event.eventType=form.eventType.data
#         event.eventDatetime=form.eventDatetime.data
#         event.eventLocation=form.eventLocation.data
#         event.eventNote=form.eventNote.data

#         exercise = event.exercises.first()
#         exercise.exerciseDuration=form.exerciseDuration.data
#         exercise.exerciseType=form.exerciseType.data
#         exercise.exerciseDistance=form.exerciseDistance.data

#         db.session.commit()
#         flash("Your news item has been updated")
#         return redirect(url_for("home_old"))
#     elif request.method == "GET":
#         form.eventType.data = event.eventType
#         form.eventDatetime.data = event.eventDatetime
#         form.eventLocation.data = event.eventLocation
#         form.eventNote.data = event.eventNote

#         exercise = event.exercises.first()
#         if event.exercises:
#             form.exerciseDuration.data = exercise.exerciseDuration
#             form.exerciseType.data = exercise.exerciseType
#             form.exerciseDistance.data = exercise.exerciseDistance
#         return render_template("new_event.html", form=form, user=current_user)

# @app.route("/delete_event/<int:id>")
# @login_required
# def delete_event(id):
#     event = eventTable.query.get_or_404(id)
#     if event.author == current_user:
#         db.session.delete(event)
#         db.session.commit()
#         flash("Event successfully deleted")
#         return redirect(url_for("home_old"))
#     else:
#         flash("User not authorized to delete")
#         return redirect(url_for("home_old"))

# # old daily_edit page to edit daily_form

# @app.route("/daily_edit/<int:id>", methods=["GET", "POST"])
# @login_required
# def daily_edit(id):
#     form = dailyForm()
#     dayEntry = dayTable.query.filter_by(id = id).first()
#     if form.validate_on_submit():
#         dayEntry.weight = form.weight.data
#         dayEntry.sleep = form.sleep.data
#         dayEntry.morning = form.morning.data
#         dayEntry.afternoon = form.afternoon.data
#         dayEntry.evening = form.evening.data
#         dayEntry.journal = form.journal.data
#         db.session.commit()
#         return redirect(url_for("daily_form"))
#     elif request.method == "GET":
#         form.date.data = dayEntry.date
#         form.weight.data = dayEntry.weight
#         form.sleep.data = dayEntry.sleep
#         form.morning.data = dayEntry.morning
#         form.afternoon.data = dayEntry.afternoon
#         form.evening.data = dayEntry.evening
#         form.journal.data = dayEntry.journal
#     else:
#         flash("There was an error with your submission")
#     exercises = db.session.query(exerciseTable).filter(exerciseTable.day_id == dayEntry.id).filter(exerciseTable.user_id == current_user.id).all()
#     contents = db.session.query(contentTable).filter(contentTable.day_id == dayEntry.id).filter(contentTable.user_id == current_user.id).all()
#     events = db.session.query(eventTable).filter(eventTable.day_id == dayEntry.id).filter(eventTable.user_id == current_user.id).all()
#     news = db.session.query(newsTable).filter(newsTable.day_id == dayEntry.id).filter(newsTable.user_id == current_user.id).all()
#     return render_template("daily_edit.html", 
#                             user=current_user, 
#                             form=form, 
#                             contents=contents, 
#                             exercises=exercises, 
#                             events=events, 
#                             news=news)


# @app.route("/ideas", methods=["GET", "POST"])
# def ideas():
#     form = ideasForm()
#     ideas = ideaTable.query.all()
#     if form.validate_on_submit():
#         ideaNote = form.ideaNote.data
#         idea = ideaTable(note=ideaNote)
#         db.session.add(idea)
#         db.session.commit()
#         ideas = ideaTable.query.all()
#         return render_template("ideas.html", form=form, ideas=ideas, user=current_user)    
#     return render_template("ideas.html", form=form, ideas=ideas, user=current_user)

# @app.route("/edit_idea/<int:id>", methods=["GET", "POST"])
# def edit_idea(id):
#     idea = ideaTable.query.get_or_404(id)
#     form = ideasForm()
#     form.ideaNote.data = idea.note
#     ideas = None
#     if form.validate_on_submit():
#         idea.note = form.ideaNote.data
#         db.session.commit()
#         return redirect(url_for("ideas"))
#     return render_template("ideas.html", form=form, ideas=ideas, user=current_user)    

# @app.route("/delete_idea/<int:id>")
# def delete_idea(id):
#     idea = ideaTable.query.get_or_404(id)
#     db.session.delete(idea)
#     db.session.commit()
#     flash("Task successfully deleted")
#     return redirect(url_for("webpage_ideas"))
