from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators

# Створення Flask форми для входу.
class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])                # Створення поля для нікнейма користувача, яке має бути заповнене обов'язково (DataRequired())
    password = PasswordField('Password', [validators.DataRequired()])         # Створення поля для вводу пароля, яке обов'язково має бути заповненим. Його особливість полягає у тому що замість символів будуть відображатися лише крапочки.
    submit = SubmitField('Log In')           # Створення 'поля', яке насправді буде кнопкою, для надсилання даних із форми.   