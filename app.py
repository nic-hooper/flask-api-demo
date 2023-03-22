from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'

with app.app_context():
    db = SQLAlchemy(app)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.String(250), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Book %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    books = Books.query.order_by(Books.date_added).all()
    return render_template('index.html',books=books)

@app.route('/add_book/', methods=['POST', 'GET'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        rating = request.form['rating']
        notes = request.form['notes']
        new_book= Books(title=title, author=author, genre=genre, rating=rating, notes=notes)

        try:
            db.session.add(new_book)
            db.session.commit()
            return redirect('/add_book/')
        except:
            return 'There was a problem adding the book'
    else:
        books = Books.query.order_by(Books.date_added).all()
        return render_template('add_book.html',books=books)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Books.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    book = Books.query.get_or_404(id)

    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.genre = request.form['genre']
        book.rating = request.form['rating']
        book.notes = request.form['notes']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating'
    else:
        return render_template('update.html', book=book)

if __name__ == "__main__":
    app.run(debug=True)