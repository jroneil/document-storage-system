from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Load configuration
app.config.from_object('app.config.Config')

# Initialize database
db = SQLAlchemy(app)

# Import routes (must be done after app and db are initialized)
from app import routes