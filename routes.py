from .. import app, login_manager
from flask import render_template, redirect, flash
from .forms import LoginForm, RegisterForm
from .database import User, session
from werkzeug.security import generate_password_hash
from flask_login import login_user, logout_user


# Створення роуту для головної сторінки.
@app.route("/")
def main():
    return render_template("main.html")




# Створення роуту для сторінки реєстрації.
@app.route("/signup", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    
    # Перевірка чи були надіслані дані із форми.
    if form.validate_on_submit():

        # Якщо так -- отримання цих даних.
        name = form.name.data
        password = form.password.data
        username = form.username.data


        user = session.query(User).where(User.username == username)
        # Перевірка чи не існує такий користувач з таким нікнеймом у БД.
        if user:
            # Якщо існує -- надсилання модального вікна з проханням спробувати увійти з цим ім'ям чи спробувати зареєструватися з інишим нікнеймом.
            flash("User exists. Please, try to login or try other username or password")
            return redirect("/login")

        else:
            # Якщо ж ні -- створення об'єкту з даними про користувача і додавання чих даних до БД.
            new_user = User(
                username=username,
                password=generate_password_hash(password),
                name=name
            )

            try:
                session.add(new_user)
                session.commit()
                return redirect("/")
            except Exception as exc:
                return f"{exc}"
            finally:
                session.close()

    else:
        # Якщо ж форма не була надіслана -- надсилання користувачу тої ж сторінки з формою для реєстрації.
        return render_template("signup.html", form=form)




# Створення роуту для сторінки для входу.
@app.route("/login", methods=["GET", "POST"])
def log_in():

    form = LoginForm()

    if form.validate_on_submit():
        password = form.password.data
        username = form.username.data

        # Пошук користувача з таким самим ім'ям, яке передане у поле вводу форми для входу.
        user = session.query(User).where(User.username == username).first()

        # Перевірка чи співпадають введені користувачем нікнейм і пароль і ті нікнейм і пароль що знаходяться у БД.
        if user and user.check_password(password):
            # Якщо так -- корстувач входить у свій акаунт.
            login_user(user)
            return redirect("/")
        
        else:
            # Якщо ж вони не співпадають, то користувачу надсилається модальне вікно з інформацією про помилку.
            flash("Wrong password or username. Please, check")
            return redirect("/login")
        
    else:
        # Якщо користувач не надіслав форму, то йому повертається та сама сторінка з формою для входу.
        return render_template("login.html", form=form)
    



# Створення роуту для виходу із акаунту користувача.
@app.route('/log_out')
def logout():
    logout_user()
    return redirect('/login')




# Дана функція підгружає всі дані про користувача за допомогою ID і надає їх функція вище. Без неї процеси логінізації і реєстрації не зможуть відбутися, оскільки не матимуть жодної інформації про користувача.
@login_manager.user_loader
def user_load(user_id):
    return session.query(User).get(int(user_id))