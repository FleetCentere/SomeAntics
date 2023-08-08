from flask import Flask, render_template, url_for, redirect, request, flash
from ProjectFiles import app #, db
from ProjectFiles.secFinancials import finSearch
from ProjectFiles.holderSearch import holderSearch
from ProjectFiles.forms import pressReleaseForm


messages = [{"title": "First Message", "content": "First message content"}, {"title": "Second message", "content": "Second message content"}]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", messages=messages)

@app.route("/about")
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
    if request.method == "POST":
        ticker = request.form["ticker"]
        startYear = request.form["startYear"]
        holderCount = request.form["holderCount"]
        companyName, financials, years = finSearch(ticker, startYear)
        holderTable, last_row, CUSIP = holderSearch(ticker, holderCount)
        return render_template("company.html", companyName=companyName, ticker=ticker, financials=financials, years=years, holderTable=holderTable, last_row=last_row)
    return render_template("companies.html")

@app.route("/content")
def content():
    return render_template("content.html")

@app.route("/ideas")
def ideas():
    return render_template("ideas.html")