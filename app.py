from flask import Flask, redirect, render_template, session, flash
from models import connect_db, db, User
from forms import SigninForm, SignupForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///acnhdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "dc981765fda04b10a3f1508208c5b8a1"
connect_db(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    

    if form.validate_on_submit():
        if (form.password.data == form.password_confirm.data):
            new_user = User.signup(password=form.password.data, username=form.username.data, email = form.email.data)

            db.session.add(new_user)
            db.session.commit()
            session["user_id"] = form.username.data
            flash("Successfully signed up!", "success")
            return redirect("/")
        else:
            flash("Error creating user. Try again later", "error")
            return redirect("/signup")
        
    return render_template("auth/signup.html", form = form)

@app.route("/signin", methods=["GET", "POST"])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        user = User.signin(password=form.password.data, username=form.username.data)
        session["user_id"] = form.username.data

        flash("Successfully signed in!", "success")
        return redirect("/")

    return render_template("auth/signin.html", form = form)

@app.route("/logout")
def logout():
    if session.get("user_id"):
        session.pop("user_id")
        flash("Successfully signed out.", "info")
    else:
        flash("Cannot sign you out", "error")
    
    return redirect("/")