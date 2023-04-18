from flask import Flask, render_template, redirect, request
from data.authors import Author
from data.students import Students
from data.users import User
from data.problems import Problems
from data import db_session
from forms.user import LoginForm, RegisterForm
from forms.problem import ProblemForm
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

#Author
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

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
        author = Author(user=user)
        db_sess.add(author)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

#Student
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
        student = Students(user=user)
        db_sess.add(student)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

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

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/problem')
def problem():
    problem_id = request.args.get('problem_id')
    return render_template('problem.html', title='Задача', problem_id=problem_id)

@app.route('/problems')
def problems():
    db_sess = db_session.create_session()
    problems = db_sess.query(Problems)
    return render_template('problems.html', title='Задачи', problems=problems)

@app.route('/problems/<int:problem_id>')
def problem_(problem_id):
    return render_template('problem.html', title='Задача', problem_id=problem_id)

@app.route('/profile')
def profile():
    if not current_user:
        return redirect('/login')
    if current_user.role == 'Автор':
        return render_template('author_profile.html', title=current_user.username)
    return render_template('student_profile.html', title=current_user.username)

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
        current_user.author.problem.append(problem)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('add_problem.html', title='Добавление задачи',
                           form=form)

def main():
    db_sess = db_session.create_session()
    # body
    db_sess.commit()

if __name__ == '__main__':
    # main()
    app.run(port=8080, host='127.0.0.0')