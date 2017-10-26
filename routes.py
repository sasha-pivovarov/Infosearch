from flask import Flask, url_for, request, render_template, redirect
from ranker import BM25Ranking



app = Flask(__name__)
rank = BM25Ranking()
rank.load()
@app.route("/")
def index():
    return render_template("main_page.jinja2")

@app.route("/search_request")
def search_request():
    query = request.args.get("query")
    quantity = int(request.args.get("quantity"))
    results = rank.process_query(query, quantity)
    return render_template("results_page.jinja2", results=results)

if __name__ == '__main__':
    app.run(debug=True)