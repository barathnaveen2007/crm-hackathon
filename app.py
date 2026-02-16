from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create database table
def init_db():
    conn = sqlite3.connect("crm.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            company TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    conn = sqlite3.connect("crm.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    conn.close()
    return render_template("index.html", customers=customers)

@app.route("/add", methods=["POST"])
def add_customer():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    company = request.form["company"]

    conn = sqlite3.connect("crm.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO customers (name, email, phone, company) VALUES (?, ?, ?, ?)",
        (name, email, phone, company)
    )
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/delete/<int:id>")
def delete_customer(id):
    conn = sqlite3.connect("crm.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)