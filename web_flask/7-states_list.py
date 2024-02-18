#!/usr/bin/python3
"""Starts a flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Displays States list HTML page"""
    states = states = storage.all(State).values()
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the connection"""
    storage.close()


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
