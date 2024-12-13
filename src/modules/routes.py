# pylint: disable=no-else-return, redefined-builtin, inconsistent-return-statements, too-many-return-statements, too-many-branches, possibly-used-before-assignment
from config import app, test_env
from flask import render_template, request, redirect, url_for, Response
from modules import database
from entities.reference import Article, Book, Inproceedings, Manual

@app.route("/")
def index():
    message = request.args.get("message", None)
    return render_template("index.html", message=message)

@app.route("/create_reference/<ref_type>", methods=["GET", "POST"])
def add_ref(ref_type):
    ref = None
    match ref_type:
        case "article":
            ref_template = Article()
            ref = Article(**(request.form))
        case "book":
            ref_template = Book()
            ref = Book(**(request.form))
        case "inproceedings":
            ref_template = Inproceedings()
            ref = Inproceedings(**(request.form))
        case "manual":
            ref_template = Manual()
            ref = Manual(**(request.form))
        case _:
            return render_template("error.html", error="Invalid reference type!")

    if request.method == "GET":
        return render_template("create_ref.html", ref=ref_template)

    if not ref.validate() or not database.add_reference(ref):
        return render_template("create_ref.html", ref=ref_template,
                               error="Invalid details")

    return redirect(url_for("index", message="createsuccess"))

@app.route("/refs")
def refs_page():
    return render_template("refs.html", references=database.get_all_references())

if test_env:
    @app.route("/reset_db")
    def reset_database():
        # This is the only import from tests
        # pylint: disable=import-outside-toplevel
        from tests import db_helper

        db_helper.reset_db()
        return "db reset", 200

@app.route("/order_references/<order>")
def order_references(order):
    refs = database.order_references(order)
    return render_template("refs.html", references=refs)

@app.route("/result")
def search_results():
    query = request.args.get('query')
    advanced_query = request.args.get('advanced_query')
    field = request.args.get('field')
    if field and advanced_query:
        refs = database.advanced_search_result(field, advanced_query)
    elif query:
        refs = database.search_result(query)
    else:
        refs = database.get_all_references()
    return render_template("refs.html", references=refs, field=field,
                           query=query, advanced_query=advanced_query, title="Search results")

@app.route("/<ref_type>/<id>")
def ref_page(ref_type, id):
    ref = database.ref_from_id(ref_type, id)
    if ref:
        return render_template("view_ref.html", ref=ref)
    else:
        return "Reference not found", 404

@app.route("/edit/<ref_type>/<id>", methods=["GET", "POST"])
def reference_edit(ref_type, id):
    ref = database.ref_from_id(ref_type, id)
    if not ref:
        return "Reference not found", 404

    if request.method == "GET":
        return render_template("edit_ref.html", ref=ref)
    try:
        edited_ref = None
        match ref_type:
            case "article":
                edited_ref = Article(**(request.form), id=int(id))
            case "book":
                edited_ref = Book(**(request.form), id=int(id))
            case "inproceedings":
                edited_ref = Inproceedings(**(request.form), id=int(id))
            case "manual":
                edited_ref = Manual(**(request.form), id=int(id))
            case _:
                return "Reference not found", 404

        if not edited_ref.validate() or not database.edit_ref(edited_ref):
            return render_template("edit_ref.html", ref=ref, error="Invalid details")
        return redirect(f"/{ref_type}/{id}")

    except ValueError:
        return render_template("edit_ref.html", ref=ref, error="Invalid details")

@app.route("/delete/<ref_type>/<id>", methods=["GET", "POST"])
def reference_delete(ref_type, id):
    ref = database.ref_from_id(ref_type, id)
    if not ref:
        return "Reference not found", 404

    if request.method == "GET":
        return render_template("delete_ref.html", ref=ref)

    if not database.delete_reference(ref):
        return render_template("error.html", error="Something went wrong.")

    return redirect(url_for("index", message="deletesuccess"))

@app.route("/advanced_search", methods=["GET", "POST"])
def advanced_search():
    if request.method == "GET":
        return render_template("advanced_search.html")
    if request.method == "POST":
        field = request.form.get("field")
        query = request.form.get("advanced_query")
        result = database.advanced_search_result(field, query)
        return render_template("refs.html", references=result, field=field,
                               advanced_query=query, title="Search results")

@app.route("/generate_bib")
def generate_bib():
    query = request.args.get('query')
    advanced_query = request.args.get('advanced_query')
    field = request.args.get('field')
    if field and advanced_query:
        refs = database.advanced_search_result(field, advanced_query)
    elif query:
        refs = database.search_result(query)
    else:
        refs = database.get_all_references()
    if refs:
        entry = ""
        for ref in refs:
            entry += ref.generate()

        response = Response(
            entry,
            mimetype="application/x-bibtex",
            content_type="application/x-bibtex; charset=utf-8",
            headers={"Content-Disposition": "attachment;filename=references.bib"}
        )
        return response
    else:
        return render_template("error.html", error="No references found.")
