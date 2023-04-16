from flask import Flask, render_template
from data.authors import Author
from data.students import Students
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Zadachnik_secret_key'

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

def main():
    db_session.global_init("db/zadachnik.db")
    db_sess = db_session.create_session()
    # body

    db_sess.commit()
    app.run(port=8080, host='127.0.0.0')

if __name__ == '__main__':
    main()