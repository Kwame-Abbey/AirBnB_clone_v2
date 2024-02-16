#!/usr/bin/python3
"""Starts a Flask web application"""
from flask import Flask
from markupsafe import escape


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """Returns a warm greeting"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Returns the string 'hbnb'"""
    return "HBNB"


@app.route("/c/<text>")
def print_c_and_text(text):
    """Returns the letter C followed by the text"""
    return f"C {escape(text).replace('_', ' ')}"


@app.route("/python/", strict_slashes=False, defaults={"text": "is cool"})
@app.route("/python/<text>", strict_slashes=False)
def print_python_and_text(text):
    """Returns Python followed by a text with a default value"""
    return f"Python {escape(text).replace('_', ' ')}"


@app.route("/number/<int:n>", strict_slashes=False)
def accept_only_integers(n):
    """Displays 'n is a number' only if n is an integer"""
    return f"{escape(n)} is a number"


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
