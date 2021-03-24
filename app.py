# pylint: disable=E0401
# pylint: disable=E1120
# pylint: disable=E1101
# pylint: disable=C0103
# pylint: disable=W0622
# pylint: disable=C0411

"""
initial app.py for flask application
"""
from functools import wraps
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from forms import BookForm
from helper import read_database_options, db
from flask import Flask, render_template, request, redirect, session, url_for

from models import Book

app = Flask(__name__)

csrf = CSRFProtect()
csrf.init_app(app)

DATABASE_OPTIONS = read_database_options()['database']

DATABASE_URL = f'postgresql://{DATABASE_OPTIONS["username"]}:\
    {DATABASE_OPTIONS["password"]}@{DATABASE_OPTIONS["host"]}:\
    {DATABASE_OPTIONS["port"]}/{DATABASE_OPTIONS["db"]}'

print(DATABASE_URL)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate()
migrate.init_app(app, db)
app.secret_key = '0fdsnfobdsf923bdvkibd2346bsdkvjcbdsw'
app.config['SECRET_KEY'] = '434534isduvcsdaouv4et6w78sdjvbcs'


def login_required(func):
    """
    login decorator
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not session.__contains__('username'):
            return redirect(url_for('login'))
        return func(*args, **kwargs)

    return decorated_function


@app.route('/')
@login_required
def book_list():
    """
    returns book list
    """
    books = Book.query.order_by('id')
    return render_template('index.html', books=books)


@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def book_add():
    """
    returns book add function
    """
    book = Book()
    book_form = BookForm(obj=book)
    if request.method == 'POST':
        if book_form.validate_on_submit():
            book_form.populate_obj(book)
            db.session.add(book)
            db.session.commit()
            return redirect('/')
    return render_template('book_edit.html', book_form=book_form)


@app.route('/update_book/<int:id>', methods=['GET', 'POST'])
@login_required
def book_update(id):
    """
    update books
    """
    book = Book.query.get(id)
    book_form = BookForm(obj=book)
    if request.method == 'POST':
        if book_form.validate_on_submit():
            book_form.populate_obj(book)
            db.session.add(book)
            db.session.commit()
            return redirect('/')
    return render_template('book_edit.html', book_form=book_form)


@app.route('/delete_book/<int:id>', methods=['GET'])
@login_required
def book_delete(id):
    """
    delete books
    """
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    inits login
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin123':
            session['username'] = username
            return redirect('/')
    return render_template('login.html')


@app.route('/logout')
def logout():
    """
    sets logout
    """
    if session.__contains__('username'):
        session.pop('username')
        return redirect('/')
    return redirect('login')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
