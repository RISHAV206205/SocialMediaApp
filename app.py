import os
import logging
from flask import Flask
from flask_login import LoginManager

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    from data_store import get_user_by_id
    return get_user_by_id(user_id)

# Import and register blueprints
from auth_routes import auth
from routes import main_routes

app.register_blueprint(auth)
app.register_blueprint(main_routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
