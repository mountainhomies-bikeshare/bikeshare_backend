import hypertrack
import secret
from flask import Flask

# Initialization
hypertrack.secret_key = secret.hypertrack_secret_key
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

