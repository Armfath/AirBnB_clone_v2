#!/usr/bin/python3
"""Basic Flask web application
"""
from flask import Flask, render_template_string, abort
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Simple greeting
    """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Simple greeting
    """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def render_c(text=None):
    f_text = text.replace('_', ' ')
    return render_template_string('C {{ content }}', content=f_text)


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def render_py(text='is_cool'):
    f_text = text.replace('_', ' ')
    return render_template_string('Python {{ content }}', content=f_text)


@app.route('/number/<n>', strict_slashes=False)
def render_number(n=None):
    try:
        n = int(n)
        return render_template_string('{{ content }} is a number', content=n)
    except:
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
