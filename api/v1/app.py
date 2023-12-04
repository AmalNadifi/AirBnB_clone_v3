#!/usr/bin/python3
"""
The following script creates a Flask app,
and registers the blueprint 'api_views' to the Flask instance app
"""

from models import storage
from api.v1.views import app_views
from werkzeug.exceptions import HTTPException
from flask import Flask
from os import getenv
from flask import jsonify
from flask_cors import CORS


app = Flask(__name__)


# Enabling CORS and allowing for origins:
CORS(app, resources={"/*": {"origins": '0.0.0.0'}})
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown_engine(exception):
    """
    The following method removes the current SQLAlchemy
    Session object after each request
    """
    storage.close()


# Updated comment for error handler
@app.errorhandler(404)
def not_found(error):
    """
    The following method returns the error msg “Not Found”
    for custom 404 error handling
    """
    response = {"error": "Not found"}
    return jsonify(response), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
