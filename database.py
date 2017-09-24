import sqlite3
from flask import g

def connect_db():

    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    """Connects to the specific database."""
    rv = sqlite3.connect("bikeshare_backend.db")#current_app.config['DATABASE'])
    rv.row_factory = dict_factory #sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
