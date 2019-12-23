from datetime import datetime
from worldlibrary import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    public_year = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.Boolean, nullable=False, default=True)
    img = db.Column(db.String(500), nullable=False)
    contributor = db.Column(db.String(500), nullable=False)
    subject = db.Column(db.String(500), nullable=False, default="Not Available")
    public_place = db.Column(db.String(500), nullable=False, default="Not Available")
    publisher = db.Column(db.String(500), nullable=False)
    isbn = db.Column(db.Integer, nullable=False)


    def __repr__(self):
            return f"Library('{self.title}', '{self.author}', '{self.public_year}', '{self.availability}' )"

class Rent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('library.id'), nullable=False)
    start_time = db.Column(db.Date, nullable=False, default=datetime.date(datetime.now()))
    end_time = db.Column(db.Date, nullable=False, default=datetime.date(datetime.now()))
    return_time = db.Column(db.Date, nullable=True)
    cost = db.Column(db.Float, nullable=False)
    overdue_rate = db.Column(db.Float, nullable=False, default=5.0)

    def __repr__(self):
            return f"Rent('{self.user_id}', '{self.book_id}', '{self.start_time}', '{self.end_time}', '{self.return_time}', '{self.cost}', '{self.overdue_rate}')"

class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    public_year = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.Boolean, nullable=False, default=True)
    img = db.Column(db.String(500), nullable=False)

    def __repr__(self):
            return f"Library('{self.title}', '{self.author}', '{self.public_year}', '{self.availability}' )"