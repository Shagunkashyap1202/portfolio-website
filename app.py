from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "shagun_portfolio_secret"
# Database Connection
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# Home Page
@app.route("/")
def home():

    conn = get_db()

    projects = conn.execute(
        "SELECT * FROM projects"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        projects=projects
    )


# Contact Form
@app.route("/contact", methods=["POST"])
def contact():

    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    conn = get_db()

    conn.execute(
        """
        INSERT INTO contacts
        (name, email, message)
        VALUES (?, ?, ?)
        """,
        (name, email, message)
    )

    conn.commit()
    conn.close()

    return redirect("/")



@app.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect("/admin-login")

    conn = get_db()

    projects = conn.execute(
        "SELECT * FROM projects"
    ).fetchall()

    conn.close()

    return render_template(
        "admin.html",
        projects=projects
    )


@app.route("/add_project", methods=["POST"])
def add_project():

    title = request.form["title"]
    description = request.form["description"]
    tech_stack = request.form["tech_stack"]
    github_link = request.form["github_link"]

    conn = get_db()

    conn.execute(
        """
        INSERT INTO projects
        (title, description, tech_stack, github_link)
        VALUES (?, ?, ?, ?)
        """,
        (title, description, tech_stack, github_link)
    )

    conn.commit()
    conn.close()

    return redirect("/admin")


@app.route("/delete_project/<int:id>")
def delete_project(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM projects WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/admin")

@app.route("/messages")
def messages():

    if not session.get("admin"):
        return redirect("/admin-login")

    conn = get_db()

    messages = conn.execute(
        "SELECT * FROM contacts ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "messages.html",
        messages=messages
    )

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "portfolio.12390":
            session["admin"] = True
            return redirect("/admin")

        return render_template(
            "admin_login.html",
            error="Invalid Username or Password"
        )

    return render_template("admin_login.html")

@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect("/")



# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)