# Imports
from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the Flask app and database
app = Flask(__name__)

# Load database credentials from environment variables
DB_USERNAME = 'root'
DB_PASSWORD = ''
DB_HOST = '127.0.0.1'
DB_PORT = 3310
DB_NAME = 'pi_home_automation'

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure the JWT secret key
app.config['JWT_SECRET_KEY'] = '67b33da88dcfd5298f42cd470b4d3deb'  # Change this!


db = SQLAlchemy(app)
jwt = JWTManager(app)


# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)

class DeviceModeOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    label = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)

class DeviceStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    mode_id = db.Column(db.Integer, db.ForeignKey('device_mode_option.id'), nullable=False)
    last_changed = db.Column(db.DateTime, default=datetime.utcnow)
    last_changed_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class ModeChangeHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    mode_id = db.Column(db.Integer, db.ForeignKey('device_mode_option.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    changed_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# Controller functions
def get_device_modes():
    devices = Device.query.all()
    data = []
    for device in devices:
        modes = DeviceModeOption.query.filter_by(device_id=device.id).all()
        status = DeviceStatus.query.filter_by(device_id=device.id).first()
        mode_label = DeviceModeOption.query.filter_by(id=status.mode_id).first().label if status else None
        device_data = {
            'label': device.label,
            'name': device.name,
            'description': device.description,
            'status': mode_label,
            'modes': [{'label': mode.label, 'name': mode.name, 'description': mode.description} for mode in modes]
        }
        data.append(device_data)
    return data

def get_user_by_credentials(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return user
    return None

def update_device_status(device_label, mode_label, user_id):
    device = Device.query.filter_by(label=device_label).first()
    if not device:
        return False, 'Device not found'

    mode = DeviceModeOption.query.filter_by(device_id=device.id, label=mode_label).first()
    if not mode:
        return False, 'Invalid mode for device'

    # Update device status
    status = DeviceStatus.query.filter_by(device_id=device.id).first()
    if status:
        status.mode_id = mode.id
        status.last_changed = datetime.utcnow()
        status.last_changed_by = user_id
    else:
        new_status = DeviceStatus(device_id=device.id, mode_id=mode.id, last_changed_by=user_id)
        db.session.add(new_status)
    
    # Log change in history
    change_history = ModeChangeHistory(device_id=device.id, mode_id=mode.id, changed_by=user_id)
    db.session.add(change_history)

    db.session.commit()
    return True, 'Device status updated'

# Routes list
@app.route('/sync', methods=['GET'])
def sync_devices():
    devices_data = get_device_modes()
    return jsonify(devices_data)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = get_user_by_credentials(username, password)
    if user:
        access_token = create_access_token(identity={'username': user.username, 'id': user.id})
        resp = make_response(jsonify({'message': 'Login successful'}))
        resp.set_cookie('access_token', access_token)
        return resp
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/get_devices', methods=['GET'])
@jwt_required()
def get_devices():
    devices_data = get_device_modes()
    return jsonify(devices_data)

@app.route('/set_device', methods=['POST'])
@jwt_required()
def set_device():
    data = request.json
    device_label = data.get('device_label')
    mode_label = data.get('mode_label')
    user_id = get_jwt_identity()['id']

    success, message = update_device_status(device_label, mode_label, user_id)
    if success:
        return jsonify({'message': message})
    else:
        return jsonify({'error': message}), 400

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='192.168.61.227')
