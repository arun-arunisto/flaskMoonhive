from flask import Flask, render_template, request, flash, session
from werkzeug.utils import secure_filename
import models as db

app = Flask(__name__)
app.secret_key = "arunisto"


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/courses")
def courses():
    if "username" in session:
        enroll = db.select_enroll()
        for i in enroll:
            flash(i, "enroll")
        courses = db.select_course()
        for i in courses:
            flash(i, "courses")
        return render_template("courses.html")
    else:
        return render_template("login.html")

@app.route("/enroll_course", methods=["POST"])
def enroll_course():
    if "username" in session:
        if request.method == "POST":
            id = request.form["id"]
            db.enroll_course(id)
            enroll = db.select_enroll()
            for i in enroll:
                flash(i, "enroll")
            courses = db.select_course()
            for i in courses:
                flash(i, "courses")
            return render_template("courses.html")
    else:
        return render_template("login.html")

@app.route("/register_user", methods=["POST"])
def register_user():
    try:
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            db.register_user(username, password)
            flash("Registered Successfully!", "register_success")
        return render_template("register.html")
    except Exception as e:
        flash("Somehing went wrong")
        print(e)
        return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_user", methods=["POST"])
def login_user():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            data =  db.select_user(username, password)
            session["username"] = data[0][0]
            print(session["username"])
            enroll = db.select_enroll()
            for i in enroll:
                flash(i, "enroll")
            courses = db.select_course()
            for i in courses:
                flash(i, "courses")
            disc = db.select_discussions()
            for d in disc:
                flash(d, "discussions")
            return render_template("index.html", data=[session["username"]])
        except Exception as e:
            print(e)
            return render_template("login.html")


@app.route("/")
def dashboard():
    if "username" in session:
        enroll = db.select_enroll()
        for i in enroll:
            flash(i, "enroll")
        courses = db.select_course()
        for i in courses:
            flash(i, "courses")
        disc = db.select_discussions()
        for d in disc:
            flash(d, "discussions")
        return render_template("index.html", data=[session["username"]])
    else:
        return render_template("login.html")

@app.route("/discussions")
def discussions():
    if "username" in session:
        disc = db.select_discussions()
        for d in disc:
            flash(d, "discussions")
        return render_template("discussions.html", data=[session["username"]])
    else:
        return render_template("login.html")

@app.route("/ask", methods=['POST'])
def ask():
    if "username" in session:
        if request.method == 'POST':
            question = request.form["question"]
            db.insert_discussions(session["username"], question, "sample answer")
            disc = db.select_discussions()
            for d in disc:
                flash(d, "discussions")
        return render_template("discussions.html", data=[session["username"]])
    else:
        return render_template("login.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/course", methods=["POST"])
def course():
    try:
        if request.method == "POST":
            course = request.form["course"]
            file = request.files["image"]
            print(course, file, secure_filename(file.filename))
            db.insert_courses(course, secure_filename(file.filename))
            file.save(f"static/assets/images/{secure_filename(file.filename)}")
            course = db.select_course()
            for i in course:
                flash(i, "course")
            return render_template("admin.html")
    except Exception as e:
        print(e)
        return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True)