from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Zadachnik_secret_key'

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

def main():
    app.run(port=8080, host='127.0.0.0')

if __name__ == '__main__':
    main()