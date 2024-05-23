from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy import Integer, String, Text, ForeignKey, Column
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'HGGeye899GhsbY737Kg47dggfT'

# ----------------------------- DATABASE ------------------------------- #
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# -------------------------------- TABLE ------------------------------- #
class Books(db.Model):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    author = Column(String(250), nullable=False)
    date = Column(String(250), nullable=False)
    price = Column(Integer)
    description = Column(Text, nullable=False)
    img_url = Column(Text, nullable=False)


with app.app_context():
    db.create_all()

CURRENT_YEAR = datetime.now().year

# ----------------------------- Routes ------------------------- #
@app.route("/")
def homepage():
    result = db.session.execute(db.select(Books))
    books = result.scalars().all()
    new_books = books[-4:]
    return render_template("index.html", books=new_books, year=CURRENT_YEAR)


@app.route("/log_in")
def log_in():
    return render_template("login.html", year=CURRENT_YEAR)


if __name__ == "__main__":
    app.run(debug=True)