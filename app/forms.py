from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class InternshipApplicationForm(FlaskForm):
    internship_id = SelectField('Internship', coerce=int, choices=[])
    resume = StringField('Resume URL', validators=[DataRequired()])
    cover_letter = TextAreaField('Cover Letter', validators=[DataRequired(), Length(min=50)])
    submit = SubmitField('Apply')

class ApplicationStatusForm(FlaskForm):
    application_id = SelectField('Application', coerce=int, choices=[])
    status = SelectField('Status', choices=[('Applied', 'Applied'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Applied')
    submit = SubmitField('Update Status')
