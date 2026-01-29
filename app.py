from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime

app = Flask(__name__)
FILE = "expenses.json"

def load_data():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def index():
    expenses = load_data()
    total = sum(float(e["amount"]) for e in expenses)
    return render_template("index.html", expenses=expenses, total=total)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        amount = request.form["amount"]
        category = request.form["category"]
        date = datetime.now().strftime("%Y-%m-%d")

        expenses = load_data()
        expenses.append({
            "title": title,
            "amount": amount,
            "category": category,
            "date": date
        })

        save_data(expenses)
        return redirect("/")

    return render_template("add.html")

@app.route("/delete/<int:index>")
def delete(index):
    expenses = load_data()
    expenses.pop(index)
    save_data(expenses)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
