from flask import Flask, redirect, render_template, session, flash, g, url_for
from models import connect_db, db, User
from forms import AccountForm, SigninForm, SignupForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///acnhdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "dc981765fda04b10a3f1508208c5b8a1"
connect_db(app)

@app.before_request
def load_user():
    if "user_id" in session:
        g.user = User.query.filter_by(username = session["user_id"]).first()
    else:
        g.user = None

@app.route("/")
def home():
    return render_template("home.html")


#
#
# Authentication
#
#

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        if (form.password.data == form.password_confirm.data):
            if User.query.filter_by(email = form.email.data).first() == None:
                if User.query.filter_by(username = form.username.data).first() == None:
                    new_user = User.signup(password=form.password.data, username=form.username.data, email = form.email.data)

                    db.session.add(new_user)
                    db.session.commit()
                    session["user_id"] = form.username.data
                    flash("Successfully signed up!", "success")
                    return redirect("/")
                else:
                    flash("Username already taken.", "error")
            else:
                flash("Email already in use.", "error")
        else:
            flash("Passwords do not match.", "error")
        return redirect("/signup")
        
    return render_template("auth/signup.html", form = form)

@app.route("/signin", methods=["GET", "POST"])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        user = User.signin(password=form.password.data, username=form.username.data)
        if user:
            session["user_id"] = form.username.data
            flash("Successfully signed in!", "success")
            return redirect("/")
        else:
            flash("Error logging in. Check your username and password.", "error")
            return redirect("/signin")

    return render_template("auth/signin.html", form = form)

@app.route("/logout")
def logout():
    if session.get("user_id"):
        session.pop("user_id")
        flash("Successfully signed out.", "info")
    else:
        flash("Cannot sign you out", "error")
    
    return redirect("/")

#
#
# User account
#
#

@app.route("/account", methods=["GET", "POST"])
def account():
    if not g.user:
        flash("Access unauthorized, please sign in.", "error")
        return redirect("/")
    
    user = g.user
    form = AccountForm(obj = user)

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
    return render_template("/user/account.html", user = user, form = form)

