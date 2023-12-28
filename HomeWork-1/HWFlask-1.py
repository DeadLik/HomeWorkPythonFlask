from flask import Flask, render_template

'''
Задание
Создать базовый шаблон для интернет-магазина, 
содержащий общие элементы дизайна (шапка, меню, подвал), 
и дочерние шаблоны для страниц категорий товаров и отдельных товаров. 
Например, создать страницы «Одежда», «Обувь» и «Куртка», используя базовый шаблон.
'''

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cloth/')
def cloth_page():
    context = {'title': 'Одежда'}
    return render_template('cloth.html', **context)


@app.route('/shoes/')
def shoes_page():
    context = {'title': 'Обувь'}
    return render_template('shoes.html', **context)


@app.route('/jacket/')
def jacket_page():
    context = {'title': 'Куртки'}
    return render_template('jacket.html', **context)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
