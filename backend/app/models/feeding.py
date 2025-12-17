from app import db
from datetime import datetime


class FeedingPlan(db.Model):
    """投喂计划表"""
    __tablename__ = 'feeding_plans'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    device_id = db.Column(db.String(50), db.ForeignKey('devices.id', ondelete='CASCADE'), nullable=False, index=True)
    time = db.Column(db.Time, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active', index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'device_id': self.device_id,
            'time': self.time.strftime('%H:%M') if self.time else None,
            'amount': self.amount,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<FeedingPlan {self.id}>'


class FeedingHistory(db.Model):
    """投喂历史表"""
    __tablename__ = 'feeding_history'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.String(50), db.ForeignKey('devices.id', ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    type = db.Column(db.String(20), nullable=False)  # auto, manual
    operator = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'device_id': self.device_id,
            'amount': self.amount,
            'time': self.time.isoformat() if self.time else None,
            'type': self.type,
            'operator': self.operator
        }
    
    def __repr__(self):
        return f'<FeedingHistory {self.id}>'
