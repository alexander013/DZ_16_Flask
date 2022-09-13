import pprint
from flask import Flask, render_template, request
from main import parce
from sqlite3 import connect
from crud import add_row
# объявление главной переменной
app = Flask(__name__)


# вывод (редеринг) главной страницы
@app.get('/index')
@app.get('/')
def index():
    return render_template('index.html')



# вывод страницы формы
@app.route('/form/')
def form():
    return render_template('forma.html')


@app.route('/result/', methods=['POST'])
def result():
    vac = request.form
    data = parce(**vac)
    dat = {**data, **vac}  # data | vac - в Python 3.10 можно сделать так
    print('orktgh0r9e-kher0h' , dat)
    dat['where'] = 'в названии вакансии' if dat['where'] == 'name' else 'в названии компании' if dat['where'] == 'company' else 'везде'
    add_row(dat)
    return render_template('contacts.html', res=dat)



if __name__ == "__main__":
    app.run(debug=True)