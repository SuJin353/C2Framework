from flask import Flask, request
from blueprints.listeners.listeners import listeners_bp
from blueprints.dashboard.dashboard import dashboard_bp

# initialize our flask app
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'

# registering blueprints
app.register_blueprint(listeners_bp, url_prefix='/listeners')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
   

# Start the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
