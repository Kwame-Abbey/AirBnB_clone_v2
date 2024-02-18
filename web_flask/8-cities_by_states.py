#!/usr/bin/python3
"""Starts a flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """Displays a HTML page"""
    states = storage.all(State).values()
    for state in states:
        if not hasattr(state, 'cities'):
            setattr(state, 'cities', state.cities)
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Closes session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
