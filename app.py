from flask import Flask, render_template, url_for, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/blockchain")
def blockchain():
    return render_template("blockchain.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        print(username, password)
        if username == "admin" and password == "admin":
            return render_template("blockchain.html")
        else:
            return render_template("login.html")
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
