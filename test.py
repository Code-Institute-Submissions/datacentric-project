import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import db

app = Flask('__name__')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sixers1983@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.debug = True
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

""" Defines secret key necessary for session """
app.secret_key = os.urandom(24)

""" --------------- Tables --------------- """

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(30), unique=True)
    
    def __repr__(self):
        return '<User: %r>' % self.username + self.email

class Items(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.Unicode(50))
    brand = db.Column(db.Unicode(20))
    size = db.Column(db.Unicode(4))
    colour = db.Column(db.Unicode(10))
    cond = db.Column(db.Unicode(15))
    gender = db.Column(db.Unicode(6))
    info = db.Column(db.Unicode(90))
    price = db.Column(db.Integer)
    contact = db.Column(db.Unicode(50))
    imageName = db.Column(db.String(100))
    imageData = db.Column(db.LargeBinary)
    
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
    return redirect(url_for('account', username=request.form['username']))

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
        flash("Username and password combination not recognised. Please try again.")
        return render_template('user.html')

@app.route('/account/<username>', methods=["GET", "POST"])
@login_required
def account(username):
    """ Displays user account once logged in """
    user = User.query.filter_by(username=username).first()
    """ Identifies items listed by user """
    myItems = Items.query.all()
    #myItems = Items.query.filter_by(contact='admin@nmtco.uk').all()
    return render_template("account.html", user=user, myItems=myItems)


@login_manager.user_loader
def load_user(user_id):
    """ Returns user object from SQLAlchemy """
    return User.query.get(int(user_id))

@app.route('/user', methods=["GET", "POST"])
def user():
    """ Redirects user to account or login page """
    if current_user.is_active:
        return render_template("account.html", user=user)
    else:
        return render_template("user.html", page_title="Log in to your account")

@app.route('/logout')
@login_required
def logout():
    """ Logs user out """
    logout_user()
    flash("You are currently logged out")
    return redirect(url_for('index'))



""" Work in progress """
@app.route('/remove_listing', methods=["GET"])
def remove_listing():
    """ Removes items from the database """
    db.session.delete(item)                 # Need to define item
    db.session.commit()
    return redirect(url_for('account'))



@app.route('/sell', methods=["GET", "POST"])
@login_required
def sell():
    return render_template("sell.html", page_title="Selling with us")

@app.route('/upload', methods=["GET", "POST"])
def upload():
    """ Uploads information to the SQL database """
    file = request.files['inputFile']
    item = Items(name=request.form['name'], brand=request.form['brand'], size=request.form['size'], \
    colour=request.form['colour'], cond=request.form['cond'], gender=request.form['gender'], \
    info=request.form['info'], price=request.form['price'], contact=request.form['contact'], \
    imageName=file.filename, imageData=file.read())
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('listed'))

@app.route('/listed')
def listed():
    return render_template("listed.html", page_title="You're all set")

db.create_all()
db.session.commit()

if __name__ == '__main__':
    app.run(
        host = os.environ.get('IP'),
        port = os.environ.get('PORT'),
        debug = True
    )