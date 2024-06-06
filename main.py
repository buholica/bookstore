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
    price = Column(Integer, nullable=False)
    old_price = Column(Integer)
    description = Column(Text, nullable=False)
    img_url = Column(Text, nullable=False)
    stars = Column(Integer)
    amount = Column(Integer, nullable=False)
    # reviews = Column(Text)


with app.app_context():
    db.create_all()


@app.context_processor
def count_cart_items():
    cart_count = len(session.get("cart", []))
    return dict(cart_count=cart_count)


@app.context_processor
def show_current_year():
    current_year = datetime.now().year
    return dict(current_year=current_year)


@app.template_filter("two_decimal")
def two_decimal_filter(number):
    return f"{number:.2f}"


# ----------------------------- Routes ------------------------- #
@app.route("/")
def homepage():
    result = db.session.execute(db.select(Books))
    books = result.scalars().all()
    new_books = books[-4:]
    return render_template("index.html", books=new_books)


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


@app.route("/product/<int:book_id>")
def show_pdp(book_id):
    requested_book = db.get_or_404(Books, book_id)
    related_books = Books.query.filter_by(type=requested_book.type).all()
    new_related_books = related_books[-4:]
    return render_template("pdp.html", book=requested_book, books=new_related_books)


@app.route("/log_in")
def log_in():
    return render_template("login.html")


@app.route("/sign_up")
def sign_up():
    return render_template("registration.html")


@app.route("/cart", methods=['GET'])
def show_cart():
    cart_items_ids = session.get("cart", [])
    cart_items = []
    cart_items_count = {}
    total_price = None

    for item_id in cart_items_ids:
        item = Books.query.filter_by(id=item_id).first()
        if item:
            if item_id in cart_items_count:
                cart_items_count[item_id] += 1
            else:
                cart_items_count[item_id] = 1
                cart_items.append(item)

    reversed_cart = cart_items[::-1]

    total_price = str(round(sum(item.price * cart_items_count[item.id] for item in cart_items), 2))
    return render_template("cart.html", cart_items=reversed_cart, total=total_price, cart_items_count=cart_items_count)


@app.route("/add-to-cart", methods=['POST'])
def add_to_cart():
    item_id = request.form.get('item_id')
    book = Books.query.filter_by(id=item_id).first()

    if book:
        if "cart" not in session:
            session["cart"] = []
        session["cart"].append(book.id)

        session.modified = True

    return redirect(url_for("show_cart"))


@app.route("/remove-item-cart", methods=['POST'])
def remove_item_from_cart():
    item_id = request.form.get("item_id")
    cart_items_ids = session.get("cart", [])

    try:
        item_id_int = int(item_id)
        if item_id_int in cart_items_ids:
            updated_cart_list = [id for id in cart_items_ids if id != item_id_int]
            session["cart"] = updated_cart_list
            session.modified = True
            print(session["cart"])
    except ValueError:
        print("The item_id is not integer.")
    return redirect(url_for("show_cart"))


@app.route("/increase-quantity", methods=['POST'])
def increase_quantity():
    item_id = request.form.get("item_id")
    item_id_int = int(item_id)

    session["cart"].append(item_id_int)
    session.modified = True

    return redirect(url_for("show_cart"))


@app.route("/decrease-quantity", methods=['POST'])
def decrease_quantity():
    item_id = request.form.get("item_id")
    item_id_int = int(item_id)

    session["cart"].remove(item_id_int)
    session.modified = True

    return redirect(url_for("show_cart"))


@app.route("/checkout")
def checkout():
    cart_items_ids = session.get("cart", [])
    cart_items = []
    cart_items_count = {}

    for item_id in cart_items_ids:
        item = Books.query.filter_by(id=item_id).first()
        if item:
            if item_id in cart_items_count:
                cart_items_count[item_id] += 1
            else:
                cart_items_count[item_id] = 1
                cart_items.append(item)

    reversed_cart = cart_items[::-1]
    total_price = str(round(sum(item.price * cart_items_count[item.id] for item in cart_items), 2))
    return render_template("checkout.html", cart_items=reversed_cart, total=total_price, cart_items_count=cart_items_count)


if __name__ == "__main__":
    app.run(debug=True)
