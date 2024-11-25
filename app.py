from flask import Flask, redirect, url_for
from blueprints.listeners.listeners import listeners_bp
from blueprints.dashboard.dashboard import dashboard_bp
import secrets

import os

# initialize our flask app
app = Flask(__name__)
foo = secrets.token_urlsafe(16)
app.secret_key = foo

# registering blueprints
app.register_blueprint(listeners_bp, url_prefix='/listeners')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
   
@app.route('/')
def index():
    return redirect(url_for('dashboard.dashboard'))


# Start the Flask app in debug mode
if __name__ == '__main__':
    if not os.path.exists("blueprints/database/"):
        os.mkdir("blueprints/database/")

    app.run(debug=True)
