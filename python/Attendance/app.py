from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ---- Database Setup ----
def init_db():
    conn = sqlite3.connect("attendance.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            name TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---- Routes ----
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        student_id = request.form.get("student_id")
        name = request.form.get("name")
        
        conn = sqlite3.connect("attendance.db")
        c = conn.cursor()
        c.execute("INSERT INTO students (student_id, name) VALUES (?, ?)", (student_id, name))
        conn.commit()
        conn.close()
        
        return redirect("/")
    return render_template("index.html")

@app.route("/records")
def records():
    conn = sqlite3.connect("attendance.db")
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    data = c.fetchall()
    conn.close()
    return render_template("records.html", students=data)

if __name__ == "__main__":
    app.run(debug=True)
