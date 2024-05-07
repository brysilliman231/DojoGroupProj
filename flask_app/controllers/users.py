from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models import trip
from flask_app.models.trip import Trip
from flask_app.controllers import trips

# hash password for safety
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():

    if not User.validate_user(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }

    id = User.save(data)

    session['user_id'] = id

    return redirect('/dashboard')

# login with validations
@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email")
        return redirect('/')
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password")
        return redirect('/')
    
    print(user.id)
    session['user_id'] = user.id

    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        'id': session['user_id']
    }

    user = User.get_by_id(data)  # Retrieve the user object
    trips = trip.Trip.get_all(data)

    return render_template("dashboard.html", user=user, trips=trips)

@app.route('/users/<int:id>')
def view_user(id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        'id': id
    }

    user = User.get_user_trips(data)
    
    return render_template("view_user.html", user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')