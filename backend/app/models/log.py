from app import db
from datetime import datetime


class Log(db.Model):
    """系统日志表"""
    __tablename__ = 'logs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)
    level = db.Column(db.String(20), nullable=False, index=True)  # INFO, WARNING, ERROR
    module = db.Column(db.String(50), nullable=False, index=True)
    operator = db.Column(db.String(50), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=False)
    ip = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'level': self.level,
            'module': self.module,
            'operator': self.operator,
            'action': self.action,
            'details': self.details,
            'ip': self.ip
        }
    
    def __repr__(self):
        return f'<Log {self.id}>'
