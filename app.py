import os
import db
from flask import Flask, render_template, redirect, request, url_for, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from base64 import b64encode
from PIL import Image
from io import BytesIO
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

""" Config for SQLAlchemy """
app = Flask('__name__')
app.url_map.strict_slashes = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sixers1983@localhost/nmtdatabase2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://vbociuqqiawsdg:5918c6bdf375a90e4371ed7b68cc4e74a8daf427415f3eba5ea1d601fdb43024@ec2-54-246-117-62.eu-west-1.compute.amazonaws.com:5432/d93ogg6ob0g3vc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.debug = True
db = SQLAlchemy(app)

""" Config for Flask Login """
login_manager = LoginManager()
login_manager.init_app(app)

""" Config for Flask Migrate """
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

""" Defines secret key necessary for session """
app.secret_key = os.urandom(24)

""" --------------- Models --------------- """

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(20), unique=True)
    email = db.Column(db.Unicode(40), unique=True)
    password = db.Column(db.Unicode(30), unique=True)
    listings = db.relationship('Items', backref='user', lazy=True)
    
    def __repr__(self):
        return '<User: %r>' % self.username + self.email + self.password

class Items(db.Model):
    __tablename__ = 'items'
    __searchable__ = ['brand']
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.Unicode(50))
    brand = db.Column(db.Unicode(30))
    size = db.Column(db.Unicode(4))
    colour = db.Column(db.Unicode(10))
    cond = db.Column(db.Unicode(15))
    gender = db.Column(db.Unicode(6))
    info = db.Column(db.Unicode(90))
    price = db.Column(db.Integer)
    contact = db.Column(db.Unicode(50))
    imageName = db.Column(db.Unicode(100))
    imageData = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    @property
    def b64_image_data(self):
        return b64encode(self.imageData).decode('utf-8')
   
    def __repr__(self):
        return '<Items: %r>' % self.name

""" --------------- Routes --------------- """

@app.route('/', methods=["GET", "POST"])
def index():
    """ Renders home page """
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
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        login_user(user, remember=True)
        return redirect(url_for('account', username=request.form['username']))
    else:
        flash("Username, email and password combination not recognised. Please try again.")
        return render_template('user.html')

@login_manager.user_loader
def load_user(user_id):
    """ Reloads user object from user ID stored in session """
    return User.query.get(int(user_id))

@app.route('/user', methods=["GET", "POST"])
def user():
    """ Redirects user to account or login page """
    if current_user.is_active:
        return redirect(url_for('account'))
    else:
        return render_template("user.html", page_title="Log in to your account")
    
@app.route('/account', methods=["GET", "POST"])
@login_required
def account():
    """ Displays user account once logged in """
    user = User.query.filter_by(username=current_user.username).first()
    """ Identifies items listed by user """
    myItems = Items.query.filter_by(user_id=current_user.id).all()
    return render_template("account.html", user=user, myItems=myItems)

@app.route('/remove_listing/<id>', methods=["GET"])
@login_required
def remove_listing(id):
    """ Removes items from the database """
    item = Items.query.get(id)
    if item.user_id == current_user.id:
        removed = Items.query.filter_by(id=int(id)).delete()
        db.session.commit()
        flash("Thanks! Your listing has been removed.")
        return redirect(url_for('account', removed=removed))
    else:
        abort(403)

@app.route('/edit_listing/<id>', methods=["GET", "POST"])
@login_required
def edit_listing(id):
    """ Enables user to update items in the database """
    item = Items.query.get(id)
    if item.user_id == current_user.id:
        if request.method == 'GET':
            return render_template("edit_listing.html", item=item)
        else:
            try:
                edited = Items.query.filter_by(id=int(id)).update(request.form)
                db.session.commit()
                flash("Thanks! Your listing has been updated.")
                return redirect(url_for('account', edited=edited))
            except:
                flash("Please ensure that all fields have been completed and that\
                an image has been re-uploaded prior to submitting changes to your listing.")
                return redirect(url_for('edit_listing', id=item.id))
    else:
        abort(403)

@app.route('/sell', methods=["GET", "POST"])
@login_required
def sell():
    """ Renders form for user to add items to the database """
    return render_template("sell.html", page_title="Selling with us")

@app.route('/upload', methods=["GET", "POST"])
def upload():
    """ Uploads information to the database """
    userId = current_user.id
    f = request.files['inputFile']
    item = Items(name=request.form['name'].title(), brand=request.form['brand'].title(), size=request.form['size'], \
    colour=request.form['colour'], cond=request.form['cond'], gender=request.form['gender'], \
    info=request.form['info'], price=request.form['price'], contact=request.form['contact'], \
    imageName=f.filename, imageData=f.read(), user_id=userId)
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('listed'))

@app.route('/listed')
@login_required
def listed():
    """ Renders page confirming upload function has worked """
    return render_template("listed.html", page_title="You're all set")

@app.route('/browse_gender')
def browse_gender():
    """ Presents items to user arranged by gender """
    mensItems = Items.query.filter_by(gender='Mens').all()
    womensItems = Items.query.filter_by(gender='Womens').all()
    unisexItems = Items.query.filter_by(gender='Unisex').all()
    return render_template("browse_gender.html", mensItems=mensItems, \
    womensItems=womensItems, unisexItems=unisexItems)

@app.route('/browse_brand')
def browse_brand():
    """ Renders 'browse by brand' html page """
    return render_template("browse_brand.html")

@app.route('/search_brand', methods=["GET"])
def search_brand():
    """ Enables user to browse items by searching keywords """
    keyword = request.args.get('keyword').title()
    searchBrand = Items.query.filter_by(brand=keyword).all()
    return render_template("browse_brand.html", searchBrand=searchBrand)

@app.route('/view_listing/<id>', methods=["GET"])
def view_listing(id):
    """ Accesses detailed views of individual items """
    item = Items.query.get(id)
    return render_template("view_listing.html", item=item)

@app.route('/logout')
def logout():
    """ Logs user out """
    logout_user()
    flash("You are currently logged out")
    return redirect(url_for('index'))

db.create_all()
db.session.commit()

if __name__ == '__main__':
    app.run(
        host = os.environ.get('IP'),
        port = os.environ.get('PORT'),
        debug = True
    )