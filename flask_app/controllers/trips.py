from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_app import app
from flask_app.models.trip import Trip
from flask_app.controllers import users

from flask_app.models import user
from flask_app.models.user import User

@app.route('/trips/add', methods=['GET', 'POST'])
def add_trip():
    if request.method == 'POST':
        # Ensure all necessary fields are included
        if not Trip.validate_trip(request.form):
            flash('Validation failed, please check your input.')
            return redirect('/trips/add')

        data = {
            'start': request.form['start'],
            'end': request.form['end'],
            'fuel': request.form['fuel'],
            'mileage': request.form['mileage'],
            'weight': request.form['weight'],
            'ppm': request.form['ppm'],
            'charge': request.form['charge'],
            'user_id': session['user_id'],
            'distance': request.form['distance']  # New distance field
        }
        Trip.save(data)
        flash('Trip added successfully.')
        return redirect('/dashboard')
    return render_template("new_trip.html")

@app.route('/trips/<int:id>')
def view_trip(id):
    data = {'trip_id': id}
    trip = Trip.get_one(data)
    if trip:
        # Calculate net profit using attributes of the trip object
        price_of_load = float(trip.charge)
        price_per_mile = float(trip.ppm)
        distance = float(trip.distance)
        mileage = float(trip.mileage)
        fuel_cost_per_gallon = float(trip.fuel)

        revenue = price_of_load + (price_per_mile * distance)
        expenses = (distance / mileage) * fuel_cost_per_gallon
        net_profit = revenue - expenses
        print("Net Profit: ", net_profit)


        # Pass the trip object and calculated net profit to the template
        return render_template("view_trip.html", trip=trip, net_profit=round(net_profit, 2))
    else:
        flash("Trip not found.")
        return redirect(url_for('dashboard'))


@app.route("/trips/<int:id>/update", methods=["GET", "POST"])
def update_trip(id):
    if request.method == 'GET':
        data = {
            "user_id": session["user_id"],
            "trip_id": id
        }
        trip = Trip.get_one(data)
        if not trip:
            flash("Trip not found.")
            return redirect(url_for('dashboard'))
        print("trip data for edit page: ", trip)
        return render_template("edit_trip.html", trip=trip)
    
    # Ensure the validation check happens in both GET (above) and POST (below)
    if not Trip.validate_trip(request.form):
        flash('Validation failed, please check your input.')
        return redirect(url_for('update_trip', id=id))
    
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
    result = Trip.update(data)
    if result:
        flash('Trip updated successfully.')
    else:
        flash('Failed to update trip.')
    
    return redirect(url_for("dashboard"))

@app.route("/trips/<int:id>/delete")
def destroy_trip(id):
    result = Trip.destroy(id)
    if result:
        flash('Trip deleted successfully.')
    else:
        flash('Failed to delete trip.')
    return redirect(url_for("dashboard"))