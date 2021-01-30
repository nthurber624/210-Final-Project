from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Email, email_validator, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    rememberMe = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    name = StringField('Name:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Retype password:', validators=[DataRequired()])
    admin = BooleanField('Are you a project administrator?')
    submit = SubmitField('Sign up!')

    def validateEmail(self, field):
        from tables import User
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

class GoalForm(FlaskForm):
    content = TextAreaField('Add a new goal:', validators=[DataRequired()])
    submit = SubmitField('Add goal')

class UpdateForm(FlaskForm):
    content = TextAreaField('Add a new update for today:', validators=[DataRequired()])
    submit = SubmitField('Add update')

class EditGoal(FlaskForm):
    newContent = TextAreaField('Edit this goal:', validators=[DataRequired()])
    submit = SubmitField('Change')

class EditUpdate(FlaskForm):
    newContent = TextAreaField('Edit this update:', validators=[DataRequired()])
    submit = SubmitField('Change')