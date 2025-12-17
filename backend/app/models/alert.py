from app import db
from datetime import datetime


class Alert(db.Model):
    """告警表"""
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(20), nullable=False, index=True)  # warning, error
    time = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    resolved = db.Column(db.Boolean, nullable=False, default=False, index=True)
    resolved_at = db.Column(db.DateTime, nullable=True)
    resolved_by = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'level': self.level,
            'time': self.time.isoformat() if self.time else None,
            'location': self.location,
            'description': self.description,
            'resolved': self.resolved,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'resolved_by': self.resolved_by
        }
    
    def __repr__(self):
        return f'<Alert {self.id}>'


class AlertNotificationSetting(db.Model):
    """告警通知设置表"""
    __tablename__ = 'alert_notification_settings'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    email = db.Column(db.Boolean, nullable=False, default=True)
    sms = db.Column(db.Boolean, nullable=False, default=False)
    push = db.Column(db.Boolean, nullable=False, default=True)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'email': self.email,
            'sms': self.sms,
            'push': self.push
        }
    
    def __repr__(self):
        return f'<AlertNotificationSetting {self.id}>'
