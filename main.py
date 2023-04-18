from flask import Flask, render_template, redirect
from data.authors import Author
from data.students import Students
from data import db_session
from forms.user import LoginForm, RegisterForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Zadachnik_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/zadachnik.db")

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template('user_role.html')

@login_manager.user_loader
def load_author(author_id):
    db_sess = db_session.create_session()
    return db_sess.query(Author).get(author_id)

#Author

#Student
@login_manager.user_loader
def load_student(student_id):
    db_sess = db_session.create_session()
    return db_sess.query(Students).get(student_id)

@app.route('/register_student', methods=['GET', 'POST'])
def reqister_student():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(Students).filter(Students.email == form.email.data).first()\
                or db_sess.query(Author).filter(Author.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = Students(
            name=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Students).filter(Students.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        user = db_sess.query(Author).filter(Author.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

def main():
    db_sess = db_session.create_session()
    # body
    db_sess.commit()

if __name__ == '__main__':
    # main()
    app.run(port=8080, host='127.0.0.0')