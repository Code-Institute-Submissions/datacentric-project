import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask('__name__')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sixers1983@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.debug = True
db = SQLAlchemy(app)

""" Defines secret key necessary for session """
app.secret_key = os.urandom(24)

#username = os.getenv('C9_USER')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(30), unique=True)
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

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
    imageName = db.Column(db.String(50))
    imageData = db.Column(db.LargeBinary)

    def __init__(self, id, name, brand, size, colour, cond, gender, info, price, contact):
        self.id = id
        self.name = name
        self.brand = brand
        self.size = size
        self.colour = colour
        self.cond = cond
        self.gender = gender
        self.info = info
        self.price = price
        self.contact = contact

# (name VARCHAR(50), brand VARCHAR(20), size VARCHAR(4), colour VARCHAR(10), cond VARCHAR(15), gender VARCHAR(6), info VARCHAR(100), price int, contact VARCHAR(50));

""" --------------- Routes --------------- """

@app.route('/', methods=["GET", "POST"])
def index():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        flash("You are now logged in to your Next Man's Treasure account")
    return render_template("index.html")

@app.route('/user', methods=["GET", "POST"])
def user():
    return render_template("user.html", page_title="Log in to your account")

@app.route('/add_user', methods=["GET", "POST"])
def add_user():
    """ Registers new users """
    user = User(request.form['username'], request.form['email'], request.form['password'])
    session['username'] = request.form['username']
    db.session.add(user)
    db.session.commit()
    session['logged_in'] = True
    return redirect(url_for('index'))

#    if request.form['password'] == 'password' and request.form['username'] == 'admin':
#        session['logged_in'] = True
#    else:
#        flash('Wrong username and/or password')

@app.route('/logout')
def logout():
    """ Logs users out from the session """
    session.pop('username', None)
    session['logged_in'] = False
    flash("You are now logged out")
    return redirect(url_for('index'))

@app.route('/sell', methods=["GET", "POST"])
def sell():
#    if request.method == 'POST':
#        if not request.form['name'] or not request.form['brand'] or not request.form['size'] or not request.form['colour'] or not request.form['cond'] or not request.form['gender'] or not request.form['info'] or not request.form['price'] or not request.form['contact']:
#            flash('Please ensure all fields are completed', 'error')
#        else:
#            item = items(request.form['name'], request.form['brand'], request.form['size'], request.form['colour'], request.form['cond'], request.form['gender'], request.form['info'], request.form['price'], request.form['contact'])
#                
#            db.session.add(item)
#            db.session.commit()
#            flash('Your item has been successfully listed')
#            return redirect(url_for('listed'))
    return render_template("sell.html", page_title="Selling with Next Man's Treasure")



""" Testing upload mechanism """
@app.route('/upload', methods=["POST"])
def upload():
    item = Items(request.form['name'], request.form['brand'], request.form['size'], request.form['colour'], request.form['cond'], request.form['gender'], request.form['info'], request.form['price'], request.form['contact'], request.files['inputFile'])
    newFile = Items(imageName=file.filename, imageData=file.read())
    db.session.add(item)
    db.session.commit()
    
    return 'Saved ' + file.filename + ' to the database.'




#@app.route('/upload', methods=["POST"])
#def upload():
#    """ Uploads files to the SQL database """
#    file = request.files['inputFile']
#    newFile = Items(name=file.filename, data=file.read())
#    db.session.add(newFile)
#    db.session.commit()
#    return file.filename

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