from hashlib import sha256
from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import CSRFProtect
from form import RegistrationForm
from models import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = b'56197a26de37619eaf59ab7be312bc1a85461b56171ff234395c315b189e0af6'
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdb.db'
db.init_app(app)


@app.cli.command('init-db')
def create():
    db.create_all()
    print('OK')


@app.route('/')
def index():
    return 'Hi'


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            password=sha256(form.password.data.encode(encoding='utf-8')).hexdigest()
        )
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрированы!')
        return redirect(url_for('index'))
    else:
        for field in form:
            for error in field.errors:
                flash(error)
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
