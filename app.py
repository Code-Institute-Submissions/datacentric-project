import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import db
from base64 import b64encode
from PIL import Image
from io import BytesIO
from flask_msearch import Search

""" Config for SQLAlchemy """
app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sixers1983@localhost/nmtdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.debug = True
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

""" Config for msearch """
MSEARCH_INDEX_NAME = 'whoosh_index'
MSEARCH_BACKEND = 'whoosh'
MSEARCH_ENABLE = True

search = Search()
search.init_app(app)

""" Defines secret key necessary for session """
app.secret_key = os.urandom(24)

""" --------------- Tables --------------- """

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(30), unique=True)
#    listings = db.relationship('Items', backref='author', lazy=True)
    
    def __repr__(self):
        return '<User: %r>' % self.username + self.email

class Items(db.Model):
    __tablename__ = 'items'
    __searchable__ = ['brand','size']
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    brand = db.Column(db.String(30))
    size = db.Column(db.String(4))
    colour = db.Column(db.String(10))
    cond = db.Column(db.String(15))
    gender = db.Column(db.String(6))
    info = db.Column(db.String(90))
    price = db.Column(db.Integer)
    contact = db.Column(db.String(50))
    imageName = db.Column(db.String(100))
    imageData = db.Column(db.LargeBinary)
#    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    @property
    def b64_image_data(self):
        return b64encode(self.imageData).decode('utf-8')
   
    def __repr__(self):
        return '<Items: %r>' % self.name


""" --------------- Routes --------------- """

@app.route('/', methods=["GET", "POST"])
def index():
    """ Home page """
    return render_template("index.html")

@app.route('/add_user', methods=["GET", "POST"])
def add_user():
    """ Registers new users """
    user = User(username=request.form['username'], email=request.form['email'], \
    password=request.form['password'])
    session['username'] = request.form['username']
    db.session.add(user)
    db.session.commit()
    login_user(user, remember=True)
    return redirect(url_for('account', username=request.form['username'], email=request.form['email']))

@app.route('/login', methods=["GET", "POST"])
def login():
    """ Logs in existing users """
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(username=username, email=email, password=password).first()
    if user:
        login_user(user, remember=True)
        return redirect(url_for('account', username=request.form['username'], email = request.form['email']))
    else:
        flash("Username, email and password combination not recognised. Please try again.")
        return render_template('user.html')

@app.route('/user', methods=["GET", "POST"])
def user():
    """ Redirects user to account or login page """
    if current_user.is_active:
        # username = ???
        return redirect(url_for('account'))
    else:
        return render_template("user.html", page_title="Log in to your account")

@app.route('/account/<username>/<email>', methods=["GET", "POST"])
@login_required
def account(username, email):
    """ Displays user account once logged in """
    user = User.query.filter_by(username=username).first()
    """ Identifies items listed by user """
    userEmail = User.query.filter_by(email=email).first()
    myItems = Items.query.all()
    #myItems = Items.query.filter_by(contact=userEmail).all()
    return render_template("account.html", user=user, myItems=myItems, userEmail=userEmail)

@app.route('/remove_listing/<id>', methods=["GET"])
def remove_listing(id):
    """ Removes items from the database """
    removed = Items.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('index', removed=removed)) # Change redirect to 'account' once login issue is resolved

@app.route('/edit_listing/<id>', methods=["GET", "POST"])
def edit_listing(id):
    if request.method == "POST":
        edited = Items.query.filter_by(id=int(id)).update({ Items.name : request.form['name'], \
        Items.cond : request.form['cond'], Items.info : request.form['info'], \
        Items.price : request.form['price'] })
        db.session.commit()
        return redirect(url_for('index', edited=edited)) # Change redirect to 'account' once login issue is resolved
    else:
        return render_template("edit_listing.html")


@login_manager.user_loader
def load_user(user_id):
    """ Returns user object from SQLAlchemy """
    return User.query.get(int(user_id))


@app.route('/logout')
@login_required
def logout():
    """ Logs user out """
    logout_user()
    flash("You are currently logged out")
    return redirect(url_for('index'))

@app.route('/sell', methods=["GET", "POST"])
@login_required
def sell():
    return render_template("sell.html", page_title="Selling with us")

@app.route('/upload', methods=["GET", "POST"])
def upload():
    """ Resizes images uploaded to the database """
    f = request.files['inputFile']
#    img = Image.open(f.stream)
#    basewidth = 300
#    wpercent = (basewidth / float(img.size[0]))
#    height = int((float(img.size[1]) * float(wpercent)))
#    img = img.resize((basewidth, height), Image.ANTIALIAS)
#    output = BytesIO()
#    img.save(output, format=format)
    """ Uploads information to the SQL database """
    item = Items(name=request.form['name'], brand=request.form['brand'], size=request.form['size'], \
    colour=request.form['colour'], cond=request.form['cond'], gender=request.form['gender'], \
    info=request.form['info'], price=request.form['price'], contact=request.form['contact'], \
#    imageName=f.filename, imageData=output.getvalue())
    imageName=f.filename, imageData=f.read())
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('listed'))

@app.route('/listed')
def listed():
    return render_template("listed.html", page_title="You're all set")

@app.route('/browse_gender')
def browse_gender():
    """ Presents items to user arranged by gender """
    mensItems = Items.query.filter_by(gender='Mens').all()
    womensItems = Items.query.filter_by(gender='Womens').all()
    unisexItems = Items.query.filter_by(gender='Unisex').all()
    return render_template("browse_gender.html", mensItems=mensItems, womensItems=womensItems, unisexItems=unisexItems)

@app.route('/browse_brand')
def browse_brand():
    return render_template("browse_brand.html")

@app.route('/search_brand', methods=["GET"])
def search_brand():
    keyword = request.args.get('keyword')
    searchBrand = Items.query.msearch(keyword,fields=['brand','size'],limit=30).all()
    return render_template("browse_brand.html", searchBrand=searchBrand)

search.create_index()
db.create_all()
db.session.commit()

if __name__ == '__main__':
    app.run(
        host = os.environ.get('IP'),
        port = os.environ.get('PORT'),
        debug = True
    )