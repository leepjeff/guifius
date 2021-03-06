import sqlite3

from models import *
from flask import g
from app import app
from contextlib import closing

from flaskext.bcrypt import Bcrypt
bcrypt = Bcrypt(app)

'''
Creates a database and sets up the schema and injects all starter
data needed to run this application.
'''
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()
'''
Initializes the connection to the database. Generally,
this should only be called once when the application begins
'''
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])



def query_db(query, args=(), one=False):
    cur = g.db.execute(query,args)
    rv = [dict((cur.description[idx][0], value)
        for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def pullUserObj(username, password):
    user = query_db('select * from users where username = ?'
            , [username], one=True)
    if (user is None):
        return None
    elif (not bcrypt.check_password_hash(user['password'], password)):
        return None
    else:
        return User(user['id'], user['username'], user['password'], user['name'], user['city'])

def curUsername(id):
    if (id is None):
        return "ERROR: Invalid Query"
    else:
        name = query_db('select username from users where id = ?', [id], one=True)
        if name is None:
            return "Invalid ID"
        return name['username']

def insert_db(query, args=(), commit=True):
    g.db.execute(query, args)
    if (commit):
        g.db.commit()

def user_exists(username):
    name = query_db('select username from users where username = ?', [username], one=True)
    if name is None:
        return False
    else:
        return True

def email_exists(email):
    email = query_db('select email from users where email = ?', [email], one=True)
    if email is None:
        return False
    else:
        return True


