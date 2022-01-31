from flask import Flask
from .database import db_session
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
