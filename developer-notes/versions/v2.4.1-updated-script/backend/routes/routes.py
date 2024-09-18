from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from controllers.device_controller import get_device_status, get_device_modes, update_device_status
from models.user_model import User

def init_routes(app):
    
    @app.route('/sync', methods=['GET'])
    def sync_devices():
        devices_data = get_device_status()
        return jsonify(devices_data)

    @app.route('/login', methods=['POST'])
    def login():
        data = request.json
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity={'username': user.username, 'id': user.id})
            resp = make_response(jsonify({'message': 'Login successful', 'access_token': access_token}))
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
