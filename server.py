from flask_app.controllers import users, trips
from flask_app import app

if __name__ == "__main__":
    app.run(port=8000, debug=True)