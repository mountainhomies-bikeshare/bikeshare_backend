import hypertrack
import secret
from flask import Flask, jsonify, request, abort

# Initialization
hypertrack.secret_key = secret.hypertrack_secret_key
app = Flask(__name__)

@app.route("/")
def hello():
    # hypertrack_bike = hypertrack.User.create(
    #     name='Bike1',
    #     email='john@example.com',
    #     phone='+15555555555',
    # )
    # print(hypertrack_bike)
    return "Hello World!"

bikes = [
    {
        'id': 1,
        'ownerid': 1,
        'location': {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -122.09037780761719,
                    37.384957792281945
                ]
            }
        },
        'description': "Awesome blue mountain bike"
    },
    {
        'id': 2,
        'ownerid': 2,
        'location': {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -122.08874702453612,
                    37.3928002484491
                ]
            }
        },
        'description': "Fantastic Red Road bike"
    },
    {
        'id': 3,
        'ownerid': 3,
        'location': {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -122.10144996643066,
                    37.38420760131265
                ]
            }
        },
        'description': "Dynamic Green racing bike"
    }
]


@app.route("/v1/get_bike_recommendations", methods=['GET'])
def get_bike_recommendations():
    # if not request.args or not request.args.get("user") or not request.args.get("location") or not request.args.get("destination"):
    #     abort(400)
    return jsonify(bikes)