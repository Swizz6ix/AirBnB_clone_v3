#!/usr/bin/python3
""" Flask App that integrates with AirBnB static HTML Template """

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
# from flasgger import Swagger


app = Flask(__name__)
# swagger = Swagger(app)

#global strict slashes
app.url_map.strict_slashes = False

#flask server environmental setup
host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', 5000)

#Registering the blueprint app_views to Flask instance app
app.register_blueprint(app_views)

#Cross-Origin Resource sharing
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})

#begin flask page rendering
@app.teardown_appcontext
def teardown(exception):
    """ After each request, this methods calls storage,close() in other words remove() on the current SQLAlchemy Session. """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """ Handles 404 errors, in the event that global error handler fails """
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)

@app.errorhandler(Exception)
def global_error_handler(error):
    """ Global Route to handle All Error Status Codes """
    if isinstance(error, HTTPException):
        if type(error).__name__ == "NotFound":
            error.description = "Not found"
        message = {'error': error.description}
        code = error.code
    else:
        message = {'error': error}
        code = 500
    return make_response(jsonify(message), code)

def setup_global_errors():
    """ This updates HTTPException Class with custom error function """
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, global_error_handler)


if __name__ == "__main__":
    """ Main Flask app """
    #initializing global error handling
    setup_global_errors()

    # start Flask app
    app.run(host=host, port=port, debug='True')