from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.fields.html5 import DateTimeField, DateField, TimeField, DateTimeLocalField
from wtforms.validators import InputRequired, Length, EqualTo
from flask_ckeditor import CKEditorField
from datetime import datetime

class RegisterForm(FlaskForm):
    firstname = StringField(label="Firstname", validators=[InputRequired()], render_kw={"placeholder": "First Name"})
    lastname = StringField(label="Lastname", render_kw={"placeholder": "Last Name"})
    username = StringField(label="Username", validators=[InputRequired(), Length(min=8, max=20)],
                           render_kw={"placeholder": "Username"})
    password = PasswordField(label="Password", validators=[InputRequired(), Length(min=8, max=20),
                                                           EqualTo("checkpassword",
                                                                   message="Password Do not Match!!!Try Again")],
                             render_kw={"placeholder": "Password"})
    checkpassword = PasswordField(label="Confirm Password", validators=[InputRequired(), Length(min=8, max=20)],
                                  render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


class AddorEditTrackerForm(FlaskForm):
    # todo
    trackerName = StringField(label="Tracker Name", validators=[InputRequired()], render_kw={"placeholder": "Deck Name"})
    trackerDesc = StringField(label="Tracker Description", render_kw={"placeholder": "Tracker Description"})
    trackerType = SelectField(label="Tracker Type", choices=[(0, 'Numeric'), (1, 'Multiple'), (2, 'Bool')], validators=[InputRequired()], render_kw={"placeholder": "Numerical, Multiple, Boolean, Time"})
    trackerSetting = StringField(label="Tracker Settings", render_kw={"placeholder": "Only for Multiple, Add CSV values"})
    submit = SubmitField("Add Tracker")


class AddLogForm(FlaskForm):
    # todo
    timestamp = DateTimeLocalField(label="timestamp", format='%Y-%m-%dT%H:%M', validators=[InputRequired()], render_kw={"placeholder": "Date-Time"})
    value = StringField(label="Value", validators=[InputRequired()], render_kw={"placeholder": "Value"})
    notes = StringField(label="Notes", render_kw={"placeholder": "Notes"})
    submit = SubmitField("Add/Edit Log")


class ReviewCardForm(FlaskForm):
    # todo
    rate = SelectField(u'Rate the Card!!!', choices=[(15, 'Easy'), (10, 'Medium'), (5, 'Hard')],
                       render_kw={"placeholder": "Rating"})
    submit = SubmitField("Submit Review")
