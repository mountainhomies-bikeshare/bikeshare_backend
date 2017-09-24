# BikeShare Backend

## Dependencies

### Hypertrack
```commandline
pip install hypertrack
```
Also, create an account with hypertrack, and use it in place of `secret.hypertrack_secret_key`

### Flask
```commandline
pip install Flask
pip install -U flask-cors
```

## Quickstart

```commandline
# If running for the first time, initialize database
FLASK_APP=main.py flask initdb
FLASK_APP=main.py flask run
```