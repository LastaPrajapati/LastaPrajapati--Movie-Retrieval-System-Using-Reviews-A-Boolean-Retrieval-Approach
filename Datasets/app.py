from flask import Flask, render_template, request
from search_engine import ReviewSearchEngine

app = Flask(__name__)

# Initialize the search engine with the absolute path to your dataset directory
search_engine = ReviewSearchEngine(r'C:\Users\Lasta\Desktop\Datasets\Dataset IR', r'C:\Users\Lasta\Desktop\Datasets\utils\review_image.json')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("query")
        results = search_engine.search(query)
        return render_template("index.html", results=results)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)