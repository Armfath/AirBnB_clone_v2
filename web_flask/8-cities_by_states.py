#!/usr/bin/python3
"""Basic Flask web application
"""
from flask import Flask, render_template
from models import storage
import os
app = Flask(__name__)
storage_type = os.getenv('HBNB_TYPE_STORAGE')


@app.teardown_appcontext
def close_database_connection(exception=None):
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states_list():
    from models.state import State
    from models.city import City
    extracted_states = sorted(storage.all(State).values(),
                              key=lambda s: s.name)
    cities_by_state = {}
    for state in extracted_states:
        if storage_type == 'db':
            cities = state.cities
        else:
            cities = state.cities()
        cities_by_state[state.id] = sorted(cities, key=lambda c: c.name)
    return render_template('8-cities_by_states.html',
            states_list=extracted_states, cities_by_state=cities_by_state)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
