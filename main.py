from flask import Flask, render_template, redirect, request
from data.users import User
from data.problems import Problems
from data import db_session
from forms.user import LoginForm, RegisterForm
from forms.problem import ProblemForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

# Шапка программы
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Zadachnik_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/zadachnik.db")

# Главная страница
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Задачник")

# Формы регистрации и входа
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

# Регистрация (Выбор роли)
@app.route("/register")
def register():
    return render_template('user_role.html', title="Выбор роли")

# Author(Автор)
@app.route('/register_author', methods=['GET', 'POST'])
def reqister_author():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            username=form.username.data,
            email=form.email.data,
            role='Автор'
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

# Student(Ученик)
@app.route('/register_student', methods=['GET', 'POST'])
def reqister_student():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            username=form.username.data,
            email=form.email.data,
            role='Ученик'
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

# Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

# Выход
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

# Блок с задачами
# Список задач
@app.route('/problems')
def problems():
    db_sess = db_session.create_session()
    problems = db_sess.query(Problems)
    return render_template('problems.html', title='Задачи', problems=problems)

# Задача через поисковик
@app.route('/problem')
def problem():
    problem_id = request.args.get('problem_id')
    return render_template('problem.html', title=f'Задача {problem_id}', problem_id=problem_id)

# Задача ссылку
@app.route('/problem/<int:problem_id>')
def problem_(problem_id):
    return render_template('problem.html', title='Задача', problem_id=problem_id)

# Личный кабинет(свой)
@app.route('/profile')
def profile():
    if not current_user:
        return redirect('/login')
    if current_user.role == 'Автор':
        db_sess = db_session.create_session()
        problems = db_sess.query(Problems).filter(Problems.author_id == current_user.id)
        return render_template('author_profile.html', title=current_user.username, problems=problems)
    return render_template('student_profile.html', title=current_user.username)

# Добавление автором задачи
@app.route('/add_problem', methods=['GET', 'POST'])
@login_required
def add_problem():
    form = ProblemForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        problem = Problems()
        problem.title = form.title.data
        problem.description = form.description.data
        problem.difficult = form.difficult.data
        current_user.problems.append(problem)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('add_problem.html', title='Добавление задачи',
                           form=form)

# Зашли в кабинет автора(не user, по id)
# Зашли в кабинет ученика(не user, по id)

# Список авторов
@app.route("/authors")
def authors():
    return render_template("authors.html")

# Новости
@app.route("/news")
def news():
    return render_template("news.html")

def main():
    db_sess = db_session.create_session()
    # body
    db_sess.commit()

if __name__ == '__main__':
    # main()
    app.run(port=8080, host='127.0.0.0')