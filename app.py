from flask import Flask, redirect, render_template, session, flash, g, url_for, request
from requests import request
import requests
from models import connect_db, db, User, Villager, Image, UserVillager
from flask_mail import Mail, Message
from forms import ImageUploadForm, SigninForm, SignupForm, UserProfileForm, VillagerSelectForm
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from  sqlalchemy.sql.expression import func
from imagekitio import ImageKit
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

#
#
# Config
#
#

# Fix Heroku connection to postgresql database
psql_uri = os.environ.get("DATABASE_URL", default="postgresql:///acnhdb")
if psql_uri and psql_uri.startswith("postgres://"):
    psql_uri = psql_uri.replace("postgres://", "postgresql://", 1)


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = psql_uri
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///acnhdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("secret_key")

app.config['MAIL_SERVER']='hayhay.link'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'acnhdb@hayhay.link'
#app.config['MAIL_PASSWORD'] = config["email_password"]
app.config["MAIL_PASSWORD"] = os.getenv("email_password")
app.config['MAIL_DEFAULT_SENDER'] = "acnhdb@hayhay.link"
app.config['MAIL_MAX_EMAILS'] = 5
app.config['MAIL_SURPRESS_SEND'] = False
app.config['MAIL_DEBUG'] = True
app.config['MAIL_ASCII_ATTACHMENTS'] = False
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

admin = Admin(app)
admin.add_views(ModelView(User, db.session), 
        ModelView(Villager, db.session), 
        ModelView(Image, db.session), 
        ModelView(UserVillager, db.session))

imagekit = ImageKit(
    #private_key = config["imagekit_private_key"],
    private_key = os.getenv("imagekit_private_key"),
    public_key = "public_4RCmJkQjOejZ8hip2KLzUCthMsI=",
    url_endpoint = 'https://ik.imagekit.io/u2glwyhen',
)

connect_db(app)

@app.before_request
def load_user():
    if "user_id" in session:
        g.user = User.query.filter_by(username = session["user_id"]).first()
    else:
        g.user = None

@app.route("/")
def home():
    rand_users = User.query.order_by(func.random()).limit(4).all()

    return render_template("home.html", users = rand_users)

@app.errorhandler(404)
def page_not_found(e):
    return (render_template('404.html'), 404)


#
#
# Authentication
#
#

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        success = True
        if (form.password.data != form.password_confirm.data):
            flash("Passwords do not match.", "error")
            success=False
        if User.query.filter_by(email = form.email.data).first() is not None:
            flash("Email already in use.", "error")
            success=False

        if User.query.filter_by(username = form.username.data).first() is not None:
            flash("Username already taken.", "error")
            success=False

        if not success:
             return render_template("auth/signup.html", form = form)

        new_user = User.signup(password=form.password.data, username=form.username.data, email = form.email.data)

        msg = Message('Welcome to acnhDB!', recipients = [f'{new_user.email}'])
        msg.html = render_template("/email/signup_email.html/")
        mail.send(msg)

        db.session.add(new_user)
        db.session.commit()
        session["user_id"] = form.username.data
        flash("Successfully signed up!", "success")

        return redirect(url_for("edit_user_profile", username = new_user.username))
        
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

@app.route("/logout/")
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

@app.route("/u/")
def all_users():
    users = User.query.all()

    return render_template("/user/users.html", users = users)

@app.route("/account", methods=["GET", "POST"])
def account():
    if not g.user:
        flash("Access unauthorized, please sign in.", "error")
        return redirect("/")
    
    user = g.user
    form = UserProfileForm(obj = user)

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
    return render_template("/user/account.html", user = user, form = form)

@app.route("/u/<username>/")
def user_profile(username):
    if g.user != None and username == g.user.username:
        user = g.user
    else:
        user = User.query.filter_by(username = username).first_or_404()

    print(user.user_villagers.first())

    return render_template("user/profile.html", user = user)

@app.route("/u/<username>/edit/", methods=["GET", "POST"])
def edit_user_profile(username):
    if g.user != None and username == g.user.username:
        user = g.user
    else:
        return (redirect("/"), 401)

    image_form = ImageUploadForm()
    # [print(villager.villagers.id) for villager in user.user_villagers]
    villager_form = VillagerSelectForm(villager_list = [villager.villagers.id for villager in user.user_villagers])

    villager_list = Villager.query.all()
    full_villager_list = [(villager.id, villager.name) for villager in villager_list]

    villager_form.villager_list.choices = full_villager_list
    if (user.profile_image[-1] != "g"):
        user_profile_form = UserProfileForm(obj = user, user_image = user.profile_image[-1])
    else:
        user_profile_form = UserProfileForm(obj = user)
        
    user_profile_form.user_image.choices = [("", "")] + full_villager_list

    if image_form.validate_on_submit():
        for file in image_form.image_file.data:
            image = imagekit.upload_file(
                file = file, 
                file_name = "Island_Image",
                options= {
                    "folder" : "/island-images/",
                    "tags": [f"{g.user.username}"],
                    "is_private_file": False,
                    "use_unique_file_name": True,
                    "response_fields": ["tags"],
                }
            )

            if (Image.query.filter_by(user_id = user.id).count() < 5):
                img = Image(image_url = image["response"]["url"], user_id = user.id)
                db.session.add(img)
                flash("Uploaded!", "success")
            else:
                flash("Could not upload images. Try again later or delete some images first.", "error")
        db.session.commit()

    if user_profile_form.validate_on_submit():
        bio = user_profile_form.bio.data
        dc = user_profile_form.dream_code.data
        fc = user_profile_form.friend_code.data
        image_id = user_profile_form.user_image.data

        user.bio = bio
        user.dream_code = dc
        user.friend_code = fc
        if image_id != "":
            user.profile_image = requests.get(f"http://acnhapi.com/v1/villagers/{image_id}").json()["icon_uri"]
        else:
            user.profile_image = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"

        db.session.commit()

    if villager_form.validate_on_submit():
        if "," in villager_form.villager_list.data: 
            data = villager_form.villager_list.data.split(",")
            UserVillager.query.filter_by(user_id = user.id).delete()

            if data != ['']:
                for villager_id in data:
                    user_villager = UserVillager(user_id = user.id, villager_id = villager_id)
                    db.session.add(user_villager)
            db.session.commit()
            flash("Successfully added villagers to your Island", "success")
            return redirect(url_for('user_profile', username = user.username))
    
    return render_template("user/edit_profile.html", 
        user = user, 
        image_form = image_form, 
        user_profile_form = user_profile_form, 
        villager_list = villager_list,
        villager_form = villager_form
    )

#
#
# Villager views
#
#

@app.route("/v/")
def all_villagers():
    villagers = Villager.query.all()

    return render_template("/villager/villagers.html", villagers = villagers)

@app.route("/v/<name>/")
def villager_profile(name):
    villager = Villager.query.filter_by(name = name).first_or_404()

    users_villagers = UserVillager.query.filter(UserVillager.villager_id == villager.id).order_by(func.random()).limit(4).all()

    return render_template("/villager/profile.html", villager = villager, users_villagers = users_villagers)

if __name__ == "__main__":
    app.run()