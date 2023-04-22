from flask import Flask, render_template, redirect, request, abort
from data.users import User
from data.problems import Problems
from data.examples import Example
from data.tests import Test
from data import db_session
from data.favourite_problems import FavouriteProblems
from forms.user import LoginForm, RegisterForm
from forms.problem import ProblemForm
from forms.author import AuthorForm
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

# Регистрация
@app.route('/register', methods=['GET', 'POST'])
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
    fav_problems = [item.problem_id for item in db_sess.query(FavouriteProblems).filter(current_user.id == FavouriteProblems.student_id)]
    return render_template('problems.html', title='Задачи', problems=problems, fav_problems=fav_problems)

# Задача через поисковик
@app.route('/problem')
def problem():
    problem_id = request.args.get('problem_id')
    return redirect(f'/problem/{problem_id}')

# Задача
@app.route('/problem/<int:problem_id>')
def problem_(problem_id):
    db_sess = db_session.create_session()
    problem = db_sess.query(Problems).filter(problem_id == Problems.id).first()
    if problem:
        return render_template('problem.html', title='Задача', problem=problem)
    return render_template('not_exist_problem.html', title='Задача', problem_id=problem_id)

# Понравилось
@app.route('/liked/<int:problem_id>')
def liked(problem_id):
    db_sess = db_session.create_session()
    fav_problems = db_sess.query(FavouriteProblems).filter(FavouriteProblems.student_id == current_user.id,
                                                           FavouriteProblems.problem_id == problem_id).first()
    if not fav_problems:
        fav_problem = FavouriteProblems(problem_id=problem_id, student_id=current_user.id)
        db_sess.add(fav_problem)
    else:
        db_sess.delete(fav_problems)
    db_sess.commit()
    return redirect('/problems')

# Личный кабинет(свой)
@app.route('/profile')
def my_profile():
    if not current_user.is_authenticated:
        return redirect('/login')
    db_sess = db_session.create_session()
    fav_problems_id = [item.problem_id for item in db_sess.query(FavouriteProblems).filter(current_user.id == FavouriteProblems.student_id)]
    if current_user.role == 'Автор':
        author_problems = db_sess.query(Problems).filter(Problems.author_id == current_user.id)
        return render_template('author_profile.html', title=current_user.username, my_problems=author_problems,
                               solved_problems=current_user.solved_problems, fav_problems=current_user.favourite_problems,
                               my_profile=True, fav_problems_id=fav_problems_id)
    return render_template('student_profile.html', title=current_user.username,
                           solved_problems=current_user.solved_problems, fav_problems=current_user.favourite_problems,
                           my_profile=True, fav_problems_id=fav_problems_id)

# Личный кабинет(чужой)
@app.route('/profile/<int:user_id>')
def profile(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(user_id == User.id).first()
    if current_user.id == user.id:
        return redirect('/profile')
    if user.role == 'Автор':
        db_sess = db_session.create_session()
        author_problems = db_sess.query(Problems).filter(Problems.author_id == user_id)
        return render_template('author_profile.html', title=user.username, my_problems=author_problems,
                               solved_problems=user.solved_problems, fav_problems=user.favourite_problems, my_profile=False)
    return render_template('student_profile.html', title=user.username,
                           solved_problems=user.solved_problems, fav_problems=user.favourite_problems, my_profile=False)


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
        problem.time_needed = form.time_needed.data
        problem.memory_needed = form.memory_needed.data
        problem.input_description = form.input_description.data
        problem.output_description = form.output_description.data
        problem.example_count = form.example_count.data
        problem.test_count = form.test_count.data
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.problems.append(problem)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect(f'/edit_examples_and_tests/{problem.id}')
    return render_template('add_problem.html', title='Добавление задачи',
                           form=form)

@app.route('/edit_problem/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_problem(id):
    form = ProblemForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        problem = db_sess.query(Problems).filter(Problems.id == id,
                                          Problems.author == current_user).first()
        if problem:
            form.title.data = problem.title
            form.description.data = problem.description
            form.difficult.data = problem.difficult
            form.time_needed.data = problem.time_needed
            form.memory_needed.data = problem.memory_needed
            form.input_description.data = problem.input_description
            form.output_description.data = problem.output_description
            form.example_count.data = problem.example_count
            form.test_count.data = problem.test_count
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        problem = db_sess.query(Problems).filter(Problems.id == id,
                                          Problems.author == current_user).first()
        if problem:
            problem.title = form.title.data
            problem.description = form.description.data
            problem.difficult = form.difficult.data
            problem.time_needed = form.time_needed.data
            problem.memory_needed = form.memory_needed.data
            problem.input_description = form.input_description.data
            problem.output_description = form.output_description.data
            problem.example_count = form.example_count.data
            problem.test_count = form.test_count.data
            db_sess.commit()
            return redirect('/profile')
        else:
            abort(404)
    return render_template('add_problem.html',
                           title='Редактирование задачи',
                           form=form)

@app.route('/delete_problem/<int:id>', methods=['GET', 'POST'])
@login_required
def problem_delete(id):
    db_sess = db_session.create_session()
    problem = db_sess.query(Problems).filter(Problems.id == id,
                                      Problems.author == current_user).first()
    if problem:
        db_sess.delete(problem)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/profile')


@app.route('/edit_examples_and_tests/<int:problem_id>', methods=['GET', 'POST'])
@login_required
def edit_examples_and_tests(problem_id):
    db_sess = db_session.create_session()
    problem = db_sess.query(Problems).filter(Problems.id == problem_id).first()
    if problem.author.id != current_user.id:
        abort(404)
    if request.method == 'POST':
        for i in range(problem.example_count):
            example = db_sess.query(Example).filter(Example.problem_id == problem_id, Example.no == i).first()
            input_data = request.form.get(f'example_input{i}')
            output_data = request.form.get(f'example_output{i}')
            if example:
                example.input = input_data
                example.output = output_data
            else:
                example = Example(input=input_data, output=output_data,
                                  problem_id=problem_id, no=i)
                db_sess.add(example)
            db_sess.commit()
        for i in range(problem.test_count):
            test = db_sess.query(Test).filter(Test.problem_id == problem_id, Test.no == i).first()
            input_data = request.form.get(f'test_input{i}')
            output_data = request.form.get(f'test_output{i}')
            if test:
                test.input = input_data
                test.output = output_data
            else:
                test = Test(input=input_data, output=output_data,
                                  problem_id=problem_id, no=i)
                db_sess.add(test)
            db_sess.commit()
        return redirect('/profile')
    return render_template('add_problem_example_and_tests.html',
                           title='Редактирование задачи',
                           example_form_count=range(problem.example_count),
                           test_form_count=range(problem.test_count))

# Стать автором
@app.route('/become_author', methods=['GET', 'POST'])
def become_author():
    form = AuthorForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if form.key.data:
            user.role = 'Автор'
        db_sess.commit()
        return redirect('/')
    return render_template('become_author.html', title='Стать автором',
                           form=form)

# Список авторов
@app.route("/authors")
def authors():
    db_sess = db_session.create_session()
    authors = db_sess.query(User).filter(User.role == "Автор")
    return render_template('authors.html', title='Авторы', authors=authors)

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