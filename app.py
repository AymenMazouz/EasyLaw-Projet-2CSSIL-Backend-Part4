from flask import Flask, request, jsonify
from search_service import SearchService


app = Flask(__name__)
search_service = SearchService()


@app.route("/")
def index():
    return "Welcome to easylaw search API"


@app.route("/supreme-court")
def search_supreme_court():
    search_query = request.args.get("search_query", "")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    search_field = request.args.get("search_field")
    subject = request.args.get("subject")
    number = request.args.get("number", type=int)
    sort_by = request.args.get("sort_by", "relevance")

    results = search_service.supreme_court_decisions(
        search_query,
        page,
        per_page,
        start_date,
        end_date,
        search_field,
        subject,
        number,
        sort_by,
    )
    return jsonify(results)


@app.route("/laws")
def search_laws():
    search_query = request.args.get("search_query", "")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    signature_start_date = request.args.get("signature_start_date")
    signature_end_date = request.args.get("signature_end_date")
    journal_start_date = request.args.get("journal_start_date")
    journal_end_date = request.args.get("journal_end_date")
    text_type = request.args.get("text_type")
    text_number = request.args.get("text_number")
    ministry = request.args.get("ministry")
    field = request.args.get("field")
    sort_by = request.args.get("sort_by", "relevance")

    results = search_service.laws(
        search_query,
        page,
        per_page,
        signature_start_date,
        signature_end_date,
        journal_start_date,
        journal_end_date,
        text_type,
        text_number,
        ministry,
        field,
        sort_by,
    )
    return jsonify(results)


@app.route("/constitution")
def search_constitution():
    search_query = request.args.get("search_query", "")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    section_name = request.args.get("section_name")
    chapter_name = request.args.get("chapter_name")
    section_number = request.args.get("section_number", type=int)
    chapter_number = request.args.get("chapter_number", type=int)
    article_number = request.args.get("article_number", type=int)

    results = search_service.constitution(
        search_query,
        page,
        per_page,
        section_name,
        chapter_name,
        section_number,
        chapter_number,
        article_number,
    )
    return jsonify(results)


@app.route("/conseil")
def search_conseil():
    search_query = request.args.get("search_query", "")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    number = request.args.get("number", type=int)
    chamber = request.args.get("chamber")
    section = request.args.get("section")
    procedure = request.args.get("procedure")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    sort_by = request.args.get("sort_by", "relevance")

    results = search_service.conseil(
        search_query,
        page,
        per_page,
        number,
        chamber,
        section,
        procedure,
        start_date,
        end_date,
        sort_by,
    )
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
