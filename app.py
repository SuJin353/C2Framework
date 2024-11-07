import json
import resources

from flask import Flask, render_template, request, redirect, url_for
from flask_restful import Api
from database.db import initialize_db

# Initialize our Flask app
app = Flask(__name__)

# Configure our database on localhost
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb+srv://21521277:phu03052003@cluster0.qxkgg.mongodb.net/'
}

# Initialize our database
initialize_db(app)

# Initialize our API
api = Api(app)

# Define the routes for each of our resources
api.add_resource(resources.Tasks, '/tasks', endpoint='tasks')


@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/payloads')
def payloads():
    return render_template('payloads.html')

@app.route('/listeners')
def listeners():
    return render_template('listeners.html')

@app.route('/connections')
def connections():
    return render_template('connections.html')

# Start the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
