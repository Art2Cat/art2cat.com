from flask_wtf import FlaskForm as BaseForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Length, Email, DataRequired, Regexp, EqualTo
from wtforms import ValidationError

from app.models import User


class LoginForm(BaseForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(BaseForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Usernames must have only letters, '
                                              'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    @staticmethod
    def validate_email(field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    @staticmethod
    def validate_username(field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class ChangePasswordForm(BaseForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm new password',
                              validators=[DataRequired()])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(BaseForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(BaseForm):
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')


class ChangeEmailForm(BaseForm):
    email = StringField('New Email', validators=[DataRequired(), Length(1, 64),
                                                 Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update Email Address')

    @staticmethod
    def validate_email(field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
