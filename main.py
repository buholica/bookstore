from flask import Flask, render_template, request, session, redirect, url_for
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
    type = Column(String(250), nullable=False)
    format = Column(String(250), nullable=False)
    price = Column(Integer)
    sale_price = Column(Integer)
    description = Column(Text, nullable=False)
    img_url = Column(Text, nullable=False)
    # stars = Column(String(250))
    # reviews = Column(Text)


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


@app.route("/faq")
def show_faq():
    return render_template("faq.html")


@app.route("/fiction")
def show_fiction():
    result = db.session.execute(db.select(Books))
    all_books = result.scalars().all()
    title = "Fiction"
    books = [book for book in all_books if book.type == "Fiction"]
    return render_template("listing.html", books=books, title=title)


@app.route("/non-fiction")
def show_nonfiction():
    result = db.session.execute(db.select(Books))
    all_books = result.scalars().all()
    title = "Non-fiction"
    books = [book for book in all_books if book.type == "Nonfiction"]
    return render_template("listing.html", books=books, title=title)


@app.route("/log_in")
def log_in():
    return render_template("login.html")


@app.route("/sign_up")
def sign_up():
    return render_template("registration.html")


@app.route("/cart")
def show_cart():
    cart_items = session.get("cart", [])
    return render_template("cart.html", cart_items=cart_items)


@app.route("/add-to-cart", methods=['POST'])
def add_to_cart():
    item_id = request.form.get('item_id')
    book_id = Books.query.filter_by(id=item_id).first()
    print(item_id)
    print(book_id)

    if item_id == book_id:
        if "cart" not in session:
            session["cart"] = []
        session["cart"].append(item_id)
    return redirect(url_for("show_cart"))



if __name__ == "__main__":
    app.run(debug=True)