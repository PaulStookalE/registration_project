from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators


# Створення форми для реєстрації. Все так само як і з формою для входу, лише додається ще одне поле -- ім'я користувача.
class RegisterForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()]) 
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Sign Up')