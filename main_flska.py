from flask import Flask, render_template, request
from main import parce


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


# @app.get('/index')
# @app.get('/')
# def index():
#     return render_template('index.html')


@app.route('/forma/')
def contacts():
    return render_template('forma.html')


@app.route('/result/')
def results():
    vac = request.form
    data = parce(**vac)
    dat = {**data, **vac}
    print(dat)
    return render_template('contacts.html', res=dat)





if __name__ == "__main__":
    app.run(debug=True)