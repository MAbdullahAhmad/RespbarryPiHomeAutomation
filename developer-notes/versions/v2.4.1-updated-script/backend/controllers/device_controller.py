from models.device_model import Device
from models.device_mode_option_model import DeviceModeOption
from models.device_status_model import DeviceStatus
from models.mode_change_history_model import ModeChangeHistory
from config.database import db
from datetime import datetime

def get_device_status():
    DEFAULT_MODE_LABEL = 'off'

    devices = Device.query.all()
    data = []
    for device in devices:
        status = DeviceStatus.query.filter_by(device_id=device.id).first()
        mode_label = DeviceModeOption.query.filter_by(id=status.mode_id).first().label if status else DEFAULT_MODE_LABEL
        device_data = {
            'label': device.label,
            'status': mode_label,
        }
        data.append(device_data)
    return data

def get_device_modes():
    DEFAULT_MODE_LABEL = 'off'

    devices = Device.query.all()
    data = []
    for device in devices:
        modes = DeviceModeOption.query.filter_by(device_id=device.id).all()
        status = DeviceStatus.query.filter_by(device_id=device.id).first()
        mode_label = DeviceModeOption.query.filter_by(id=status.mode_id).first().label if status else DEFAULT_MODE_LABEL
        device_data = {
            'label': device.label,
            'name': device.name,
            'description': device.description,
            'status': mode_label,
            'modes': [{'label': mode.label, 'name': mode.name, 'description': mode.description} for mode in modes]
        }
        data.append(device_data)
    return data

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
