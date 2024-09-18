from flask import Flask
from flask_jwt_extended import JWTManager
from routes.routes import init_routes
from config.database import db

# Initialize the Flask app
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pi_home_automation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '67b33da88dcfd5298f42cd470b4d3deb'

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# Initialize routes
init_routes(app)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
