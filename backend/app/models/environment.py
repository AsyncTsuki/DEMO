from app import db
from datetime import datetime


class EnvironmentData(db.Model):
    """环境数据表"""
    __tablename__ = 'environment_data'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)
    temperature = db.Column(db.Float, nullable=False)
    dissolved_oxygen = db.Column(db.Float, nullable=False)
    ph = db.Column(db.Float, nullable=False)
    water_flow = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'temperature': self.temperature,
            'dissolvedOxygen': self.dissolved_oxygen,
            'ph': self.ph,
            'waterFlow': self.water_flow
        }
    
    def __repr__(self):
        return f'<EnvironmentData {self.id}>'


class EnvironmentThreshold(db.Model):
    """环境告警阈值表"""
    __tablename__ = 'environment_thresholds'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    temperature_min = db.Column(db.Float, nullable=False, default=18.0)
    temperature_max = db.Column(db.Float, nullable=False, default=28.0)
    dissolved_oxygen_min = db.Column(db.Float, nullable=False, default=5.0)
    dissolved_oxygen_max = db.Column(db.Float, nullable=False, default=8.0)
    ph_min = db.Column(db.Float, nullable=False, default=7.0)
    ph_max = db.Column(db.Float, nullable=False, default=8.0)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'temperature': {
                'min': self.temperature_min,
                'max': self.temperature_max
            },
            'dissolvedOxygen': {
                'min': self.dissolved_oxygen_min,
                'max': self.dissolved_oxygen_max
            },
            'ph': {
                'min': self.ph_min,
                'max': self.ph_max
            }
        }
    
    def __repr__(self):
        return f'<EnvironmentThreshold {self.id}>'
