import hypertrack
from flask import Flask, jsonify, g, request
import database
import secret
import uuid
import requests
import json

# Initialization
hypertrack.secret_key = secret.hypertrack_secret_key
app = Flask(__name__)

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
    id = str(uuid.uuid4())
    database.get_db().execute("INSERT INTO bikes VALUES (?, ?, ?, ?, ?, ?)",
                                       (id, request.json["hypertrack_id"], request.json["account_id"], request.json["description"], False, None, ))
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
    accounts = []
    for row in res.fetchall():
        account = {}
        account["id"] = row[0]
        account["name"] = row[1]
        account["email"] = row[2]
        account["phone"] = row[3]
        accounts.append(account)
    return jsonify(accounts)

@app.route("/v1/list_all_bikes", methods=['GET'])
def list_all_bikes():
    res = database.get_db().execute("SELECT * FROM bikes")
    bikes = []
    for row in res.fetchall():
        bike = {}
        bike["id"] = row[0]
        bike["hypertrack_id"] = row[1]
        bike["account_id"] = row[2]
        bike["description"] = row[3]
        bike["is_on_loan"] = row[4]
        bike["loan_account_id"] = row[5]
        bikes.append(bike)
    return jsonify(bikes)


##############
### HELPER ###
##############

def response_success():
    return jsonify({"status": 0})