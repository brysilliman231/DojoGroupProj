from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask import request

from flask_app.models import  trip, user
from flask_app.models.trip import Trip

# forces to use special characters in email
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.adventures = [] # holds adventure list

# get all from users database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('trucking').query_db(query)
        
        users = []
        for row in results:
            users.append(cls(row))

        return users
# save a new user

    @classmethod
    def save(cls, data):
        query = """INSERT INTO
                        users
                    (first_name, last_name, email, password)
                        VALUES
                    ( %(first_name)s, %(last_name)s, %(email)s, %(password)s)"""
        return connectToMySQL('trucking').query_db(query, data)

# grab user with email
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('trucking').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

# grab user by user id
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('trucking').query_db(query,data)
        return cls(results[0])

# registartion validations
    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        
        results = connectToMySQL('trucking').query_db(query,user)

        if len(results) >= 1:
            flash("E-mail already taken.")
            is_valid = False

        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email format")
            is_valid = False

        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters")
            is_valid= False
        
        if len(user['last_name']) < 2:
                flash("Last name must be at least 2 characters")
                is_valid= False

        if len(user['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid= False
        if user['password'] != user['confirm']:
            flash("Passwords do not match")

        return is_valid

# grab all trips from a user using user id
    @classmethod
    def get_user_trips(cls, data):
        query = "SELECT * FROM users LEFT JOIN trips ON users.id=trips.user_id WHERE users.id=%(id)s"
        results = connectToMySQL('trucking').query_db(query, data)
        user = cls(results[0])
        for trip in results:
            trip_data = {
                'id': trip['trips.id'],
                'start': request.form['start'],
                'end': request.form['end'],
                'fuel': request.form['fuel'],
                'mileage': request.form['mileage'],
                'weight': request.form['weight'],
                'ppm': request.form['ppm'],
                'charge': request.form['charge'],
                'user_id': request.form['user_id']
            }
            this_trip = Trip(trip_data)
            user.trips.append(this_trip)
        return user



class UserProfile:
    @classmethod
    def get_by_user_id(cls, user_id):
        query = "SELECT * FROM user_profiles WHERE user_id = %(user_id)s;"
        data = {'user_id': user_id}
        result = connectToMySQL('trucking').query_db(query, data)
        if result:
            return cls(result[0])
        return None

    @classmethod
    def update_or_create(cls, user_id, truck_type, favorite_food, fun_fact):
        # Check if profile exists
        existing_profile = cls.get_by_user_id(user_id)
        if existing_profile:
            query = """
                UPDATE user_profiles SET truck_type = %(truck_type)s, 
                favorite_food = %(favorite_food)s, fun_fact = %(fun_fact)s 
                WHERE user_id = %(user_id)s;
            """
        else:
            query = """
                INSERT INTO user_profiles (user_id, truck_type, favorite_food, fun_fact) 
                VALUES (%(user_id)s, %(truck_type)s, %(favorite_food)s, %(fun_fact)s);
            """
        data = {
            'user_id': user_id,
            'truck_type': truck_type,
            'favorite_food': favorite_food,
            'fun_fact': fun_fact
        }
        return connectToMySQL('trucking').query_db(query, data)

    def __init__(self, data):
        self.user_id = data['user_id']
        self.truck_type = data['truck_type']
        self.favorite_food = data['favorite_food']
        self.fun_fact = data['fun_fact']