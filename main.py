import hypertrack
from flask import Flask, jsonify, g, request
import database
import secret
import uuid
import requests
import json
import constants
from flask_cors import CORS

# Initialization
hypertrack.secret_key = secret.hypertrack_secret_key
app = Flask(__name__)
CORS(app)

@app.cli.command('prod')
def prod_command():
    app.run(host='0.0.0.0')

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


####################
### MAIN METHODS ###
####################

@app.route("/v1/register_account", methods=['POST'])
def register_account():
    id = str(uuid.uuid4())
    database.get_db().execute("INSERT INTO accounts VALUES (?, ?, ?, ?)",
                              (id, request.json["name"], request.json["email"], request.json["phone"]))
    database.get_db().commit()
    return jsonify({"id": id})

@app.route("/v1/register_bike", methods=['POST'])
def register_bike():
    id = str(uuid.uuid4()) if "id" not in request.json else request.json["id"]
    is_on_loan = False if "is_on_loan" not in request.json else request.json["is_on_loan"]
    loan_account_id = None if "loan_account_id" not in request.json else request.json["loan_account_id"]
    database.get_db().execute("INSERT INTO bikes VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                       (id, request.json["ht_id"], request.json["account_id"], request.json["description"],
                                        is_on_loan, loan_account_id, request.json["price"], request.json["deadline"]))
    database.get_db().commit()
    return jsonify({"id": id})

@app.route("/v1/get_bike_recommendations", methods=['POST'])
def get_bike_recommendations():
    # if not request.args or not request.args.get("user") or not request.args.get("location") or not request.args.get("destination"):
    #     abort(400)
    headers = {"Authorization": "token " + secret.hypertrack_secret_key}
    all_bikes = requests.get('https://api.hypertrack.com/api/v1/users/nearby/?location=' + str(request.json["coordinates"][0])
                       + "," + str(request.json["coordinates"][1]), headers=headers).content
    all_bikes = json.loads(all_bikes)

    return jsonify(all_bikes["results"][:3])

@app.route("/v1/get_bike_recommendations_constants", methods=['GET'])
def get_bike_recommendations_constants():
    return jsonify(constants.bikes)

@app.route("/v1/rent_bike/<string:bike_id>", methods = ['GET'])
def rent_bike(bike_id):
    database.get_db().execute("UPDATE bikes SET is_on_loan = ? WHERE id = ?",
                                       (True, bike_id))
    database.get_db().commit()
    return response_success()

@app.route("/v1/return_bike/<string:bike_id>", methods = ['GET'])
def return_bike(bike_id):
    database.get_db().execute("UPDATE bikes SET is_on_loan = ? WHERE id = ?",
                                       (False, bike_id))
    database.get_db().commit()
    return response_success()


#################
### DEBUGGING ###
#################

@app.route("/v1/list_all_accounts", methods=['GET'])
def list_all_users():
    res = database.get_db().execute("SELECT * FROM accounts")
    return jsonify(res.fetchall())

@app.route("/v1/list_all_bikes", methods=['GET'])
def list_all_bikes():
    res = database.get_db().execute("SELECT * FROM bikes")
    return jsonify(res.fetchall())


##############
### HELPER ###
##############

def response_success():
    return jsonify({"status": 0})