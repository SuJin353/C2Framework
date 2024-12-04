from flask import Flask, redirect, url_for
from blueprints.listeners.listeners import *
from blueprints.dashboard.dashboard import dashboard_bp
from blueprints.agents.agents import agents_bp
from blueprints.payload.payload import payload_bp

import secrets
import argparse
# initialize our flask app
app = Flask(__name__)
foo = secrets.token_urlsafe(16)
app.secret_key = foo

# registering blueprints
app.register_blueprint(listeners_bp, url_prefix='/listeners')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(agents_bp, url_prefix='/agents')
app.register_blueprint(payload_bp, url_prefix='/payload')
   
@app.route('/')
def index():
    return redirect(url_for('dashboard.dashboard'))

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Run Flask app with specified host and port.')
    parser.add_argument('--host', type=str, required=True, help='Host IP address')
    parser.add_argument('--port', type=int, required=True, help='Port number')

    # Parse the arguments
    args = parser.parse_args()

    name = "test_2"
    bind_address = args.host
    bind_port = args.port
    listener = Listener(name, type, bind_address, bind_port)
    listener.save()

    app.run(host = bind_address, port = bind_port)

# Start the Flask app in debug mode
if __name__ == '__main__':
    main()