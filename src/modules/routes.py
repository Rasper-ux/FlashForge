from config import app, db, test_env
from flask import render_template, request, redirect, url_for
from modules import database
from sqlalchemy import text

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_reference/article", methods=["GET", "POST"])
def add_ref():
    if request.method == "GET":
        return render_template("create_reference_article.html")
    if request.method == "POST":
        failed = False
        try:
            author = request.form.get("author")
            title = request.form.get("title")
            journal = request.form.get("journal")
            year = int(request.form.get("year"))

        except ValueError:
            return render_template("create_reference_article.html", error=True, error_message="Invalid details")
        
        if len(author) > 100:
            failed = True
            message = "Name of author cannot exceed 100 characters"
        
        if len(title) > 500:
            failed = True
            message = "Title cannot exceed 500 characters"
        
        if len(journal) > 100:
            failed = True
            message = "Name of journal cannot exceed 100 characters"
        
        if year < 1900 or year > 2099:
            failed = True
            message = "Year must be set between 1900 and 2099"
        
        if failed:
            return render_template("create_reference_article.html", error=True, error_message=message)

        if database.add_article(author, title, journal, year):
            return redirect(url_for("index"))
        else:
            return render_template("create_reference_article.html", error=True, error_message="Invalid details")
        
@app.route("/refs")
def refs():
    refs=database.get_all_articles()
    return render_template("refs.html", references=refs)

if test_env:
    print("should be here!!!")
    @app.route("/reset_db")
    def reset_database():
        database.reset_db()
        return "db reset", 200

@app.route("/result")
def search_results():
    query = request.args.get('query')
    result = database.search_result(query)
    return render_template("search_results.html", references = result)
