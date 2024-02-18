#!/usr/bin/python3
"""Starts a web application
"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Closes session"""
    storage.close()


@app.route('/states', strict_slashes=False, defaults={'id': None})
@app.route('/states/<id>')
def cities_by_states(id):
    """ displays list of cities by state id"""
    states = storage.all(State).values()
    if id is None:
        return render_template('7-states_list.html', states=states)
    for state in states:
        if state.id == id:
            return render_template('9-states.html', state=state)
    return render_template('9-states.html', state=None)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
