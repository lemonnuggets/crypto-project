from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)


@app.route("/")
def index():
    return redirect("/home")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/blockchain", methods=["GET", "POST"])
def blockchain():
    return render_template("blockchain.html")


if __name__ == "__main__":
    app.run(debug=True)
