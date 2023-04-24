#!/usr/bin/python3
"""Basic Flask web application
"""
from flask import Flask, render_template
from models import storage
app = Flask(__name__)


@app.teardown_appcontext
def close_database_connection(exception=None):
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list(n=None):
    from models.state import State
    extracted_states = storage.all(State).values()
    return render_template('7-states_list.html', states_list=extracted_states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
