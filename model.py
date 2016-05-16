
'''
        model.py
'''
from app import app, g
import sqlite3


def db_content():
    return sqlite3.connect(app.config['DATABASE_PATH'])

@app.before_request
def before_request():
    g.db = db_content()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g,'db')
    if db is not None:
        db.close()


