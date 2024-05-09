from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash , request
from flask_app.models import user
from flask_app.models import trip


class Trip:
    def __init__( self , data ):
        self.id = data['id']
        self.start = data['start']
        self.end = data['end']
        self.fuel = data['fuel']
        self.mileage = data['mileage']
        self.weight = data['weight']
        self.ppm = data['ppm']
        self.charge = data['charge']
        self.user_id = data['user_id']
        self.user = None

    @classmethod
    def get_all(cls, data):
        query = """
                SELECT * FROM trips
                LEFT JOIN users
                ON trips.user_id = users.id
        """
        results = connectToMySQL('trucking').query_db(query, data)

        trips = []

        for row in results:
            this_trip = cls(row)

            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
            }
            this_trip.user = user.User(user_data)

            trips.append(this_trip)

        return trips
    
    @classmethod
    def save(cls, data):
        query = """
                    INSERT INTO trips
                    (start, end, fuel, mileage, weight, ppm, charge, user_id)
                    VALUES (%(start)s, %(end)s, %(fuel)s, %(mileage)s, %(weight)s, %(ppm)s, %(charge)s, %(user_id)s);
                """
        return connectToMySQL('trucking').query_db(query, data)
    @classmethod
    def get_one(cls, data):
        print("data being passed into get one: ",data)
        query =  """SELECT * FROM trips LEFT JOIN users
                    ON trips.user_id = users.id
                    WHERE trips.id = %(trip_id)s;"""
        results = connectToMySQL('trucking').query_db(query, data)
    
        print("results from get one: ", results)

        if results:
            this_trip = cls(results[0])
            return this_trip
        else:
            # Handle the case where results is not as expected
            return None

    
    @classmethod
    def update(cls, data):
        print("data in update: ", data)
        query = """
                    UPDATE trips SET
                    VALUES
                    start = %(start)s,
                    end = %(end)s,
                    fuel = %(fuel)s,
                    mileage = %(mileage)s,
                    weight = %(weight)s,
                    ppm = %(ppm)s,
                    charge = %(charge)s,
                    user_id = %(user_id)s);
                    WHERE
                    trips.id = %(trip_id)s
                """
        result = connectToMySQL('trucking').query_db(query,data)
        print("result in update", result)
        return result
    
    @classmethod
    def destroy(cls, id):
        query = "DELETE FROM trips WHERE id=%(id)s"
        return connectToMySQL('trucking').query_db(query, {"id":id})
    
    @staticmethod
    def validate_trip(trip):
        is_valid = True
        if len(trip['start']) < 1: #cannot be blank
            flash("Gave your trip a start!")
            is_valid= False
        if len(trip['end']) < 1: # cannot be blank
            flash("Give your trip an end!")
            is_valid= False
        if len(trip['fuel']) < 1: # cannot be blank
            flash("How much Fuel!")
            is_valid= False
        if len(trip['mileage']) < 1: #cannot be blank
            flash("How many miles!")
            is_valid= False
        if len(trip['weight']) < 1: #cannot be blank
            flash("How much weight!")
            is_valid= False
        if len(trip['ppm']) < 1: #cannot be blank
            flash("Pay Per Mile!")
            is_valid= False
        if len(trip['charge']) < 1: #cannot be blank
            flash("How much are your charging!")
            is_valid= False
        return is_valid