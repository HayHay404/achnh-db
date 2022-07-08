from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SelectField, MultipleFileField, TextAreaField
from wtforms.validators import InputRequired, Email, Length


class SigninForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class SignupForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    password_confirm = PasswordField("Confirm Password", validators=[InputRequired()])

class UserProfileForm(FlaskForm):
    user_image = SelectField("Profile Image")
    bio = TextAreaField("Bio", validators=([Length(max=280)]))
    friend_code = StringField("Friend Code", validators=[Length(max=12)])
    dream_code = StringField("Dream Code", validators=[Length(max=12)])

class ImageUploadForm(FlaskForm):
    image_file = MultipleFileField("Upload Banner Images", validators=[Length(max=5)])
    
    