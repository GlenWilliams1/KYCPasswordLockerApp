from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    security_question1 = StringField('Security Question 1', validators=[DataRequired()])
    security_answer1 = StringField('Security Answer 1', validators=[DataRequired()])
    security_question2 = StringField('Security Question 2', validators=[DataRequired()])
    security_answer2 = StringField('Security Answer 2', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SecurityQuestionsForm(FlaskForm):
    answer1 = StringField('Answer 1', validators=[DataRequired()])
    answer2 = StringField('Answer 2', validators=[DataRequired()])
    submit = SubmitField('Submit')