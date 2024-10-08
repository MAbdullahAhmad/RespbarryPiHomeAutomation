from config.database import db
from datetime import datetime

class ModeChangeHistory(db.Model):
    __tablename__ = 'mode_change_history'

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    mode_id = db.Column(db.Integer, db.ForeignKey('device_mode_options.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    changed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
