from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_app import app
from flask_app.models.trip import Trip
from flask_app.controllers import users

from flask_app.models import user
from flask_app.models.user import User


@app.route('/trips/add', methods=['GET', 'POST'])
def add_trip():
    if request.method == 'GET':
        return render_template("new_trip.html")

    if not Trip.validate_trip(request.form):
        flash("Invalid data. Please check your input.", "error")
        return redirect("/trips/add")  # Redirect back to the add adventure page if data is invalid

    data = {
        'start': request.form['start'],
        'end': request.form['end'],
        'fuel': request.form['fuel'],
        'mileage': request.form['mileage'],
        'weight': request.form['weight'],
        'ppm': request.form['ppm'],
        'charge': request.form['charge'],
        'user_id': request.form['user_id']
    }
    Trip.save(data)
    flash("Trip added successfully.", "success")
    return redirect("/dashboard")

@app.route("/trips/<int:id>")
def view_trip(id):
    data = {
        'trip_id': id,
        'user_id': session["user_id"]
    }
    trip = Trip.get_one(data)
    return render_template("view_trip.html", trip=trip)

@app.route("/trips/<int:id>/update", methods=["GET", "POST"])
def update_trip(id):
    if request.method == 'GET':
        data = {
            "user_id": session["user_id"],
            "trip_id": id
        }
        trip = Trip.get_one(data)
        print("trip data for edit page: ", trip)
        return render_template("update_trip.html", trip=trip)
    
    if not Trip.validate_trip(request.form):
        return redirect('/trips/{id}/update')
    
    data = {
        'trip_id': id,
        'start': request.form['start'],
        'end': request.form['end'],
        'fuel': request.form['fuel'],
        'mileage': request.form['mileage'],
        'weight': request.form['weight'],
        'ppm': request.form['ppm'],
        'charge': request.form['charge'],
    }
    trip = Trip.update(data)
    return redirect("/dashboard")

@app.route("/trips/<int:id>/delete")
def destroy_trip(id):
    Trip.destroy(id)
    return redirect("/dashboard")