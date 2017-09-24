import sqlite3
from flask import g

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect("bikeshare_backend.db")#current_app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

