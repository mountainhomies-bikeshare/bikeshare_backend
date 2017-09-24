import hypertrack
from flask import Flask, jsonify, g
from constants import bikes
import database
import secret
# Initialization


hypertrack.secret_key = secret.hypertrack_secret_key
app = Flask(__name__)

@app.cli.command('initdb')
def initdb_command():
    def init_db():
        db = database.get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route("/")
def hello():
    # hypertrack_bike = hypertrack.User.create(
    #     name='Bike1',
    #     email='john@example.com',
    #     phone='+15555555555',
    # )
    # print(hypertrack_bike)
    return "Hello World!"


@app.route("/v1/get_bike_recommendations", methods=['GET'])
def get_bike_recommendations():
    # if not request.args or not request.args.get("user") or not request.args.get("location") or not request.args.get("destination"):
    #     abort(400)
    return jsonify(bikes)