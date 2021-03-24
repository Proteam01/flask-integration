from flask_migrate import Migrate

from forms import BookForm
from helper import read_database_options, db
from flask import Flask, render_template, request, redirect

from models import Book

app = Flask(__name__)

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
app.config['SECRET_KEY'] = '434534isduvcsdaouv4et6w78sdjvbcs'


@app.route('/')
def book_list():
    books = Book.query.order_by('id')
    return render_template('index.html', books=books)


@app.route('/add_book', methods=['GET', 'POST'])
def book_add():
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
def book_update(id):
    book = Book.query.get(id)
    book_form = BookForm(obj=book)
    if request.method == 'POST':
        if book_form.validate_on_submit():
            book_form.populate_obj(book)
            db.session.add(book)
            db.session.commit()
            return redirect('/')
    return render_template('book_edit.html', book_form=book_form)



if __name__ == '__main__':
    app.run(port=5000, debug=True)
