from flask_wtf import FlaskForm as BaseForm
from wtforms import StringField, SubmitField, BooleanField, SelectMultipleField, widgets
from wtforms.validators import DataRequired

class MultiCheckboxField(SelectMultipleField):
    #widgets = widgets.ListWidget(prefix_label=False)

    option_widget = widgets.CheckboxInput()

class NameForm(BaseForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(BaseForm):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class PostForm(BaseForm):
    title = StringField('title')
    article = StringField('Enter your content')
    tag_list =['test','test1']
    tags = MultiCheckboxField('Label', choices=[(x,x) for x in tag_list])
    submit = SubmitField('Submit')
