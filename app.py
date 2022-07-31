from flask import Flask, request, render_template, redirect, session
from flask_session import Session
from cs50 import SQL

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use in server filesystem 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///bookstore.db")


@app.route('/')
def index():
    books = db.execute("SELECT * FROM books")

    return render_template("books.html", books=books)


@app.route('/cart', methods=["POST", "GET"])
def cart():
    if 'cart' not in session:
        session["cart"] = []

    if request.method == "POST":
        id = request.form.get("id")

        if id:
            session["cart"].append(id)
        return redirect('/cart')

    books = db.execute("SELECT * FROM books WHERE id IN (?)", session["cart"])
    return render_template("cart.html", books=books)