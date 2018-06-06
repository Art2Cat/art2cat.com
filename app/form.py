from flask_wtf import FlaskForm as BaseForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired


class NameForm(BaseForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(BaseForm):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class PostForm(BaseForm):
    title = StringField('title', validators=[DataRequired()])
    article = StringField('content', validators=[DataRequired()])
    tags = SelectField(choices=['test','test1'])
