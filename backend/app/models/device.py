from app import db
from datetime import datetime
import json


class Device(db.Model):
    """设备表"""
    __tablename__ = 'devices'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default='offline', index=True)
    active = db.Column(db.Boolean, nullable=False, default=True)
    location = db.Column(db.String(100), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    
    # 关联
    configs = db.relationship('DeviceConfig', backref='device', lazy='dynamic', cascade='all, delete-orphan')
    feeding_plans = db.relationship('FeedingPlan', backref='device', lazy='dynamic', cascade='all, delete-orphan')
    feeding_histories = db.relationship('FeedingHistory', backref='device', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'status': self.status,
            'active': self.active,
            'location': self.location,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_updated': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Device {self.id}>'


class DeviceConfig(db.Model):
    """设备配置表"""
    __tablename__ = 'device_configs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.String(50), db.ForeignKey('devices.id', ondelete='CASCADE'), nullable=False)
    config = db.Column(db.JSON, nullable=False, default=dict)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'device_id': self.device_id,
            'config': self.config
        }
    
    def __repr__(self):
        return f'<DeviceConfig {self.id}>'


class DeviceLinkageConfig(db.Model):
    """设备联动配置表"""
    __tablename__ = 'device_linkage_config'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trigger_type = db.Column(db.String(50), nullable=False, default='time')
    interval = db.Column(db.Integer, nullable=False, default=60)
    related_devices = db.Column(db.JSON, nullable=False, default=list)
    auto_adjust = db.Column(db.Boolean, nullable=False, default=False)
    temp_threshold = db.Column(db.Float, nullable=False, default=25.0)
    oxygen_threshold = db.Column(db.Float, nullable=False, default=6.0)
    ph_threshold = db.Column(db.Float, nullable=False, default=7.5)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'triggerType': self.trigger_type,
            'interval': self.interval,
            'relatedDevices': self.related_devices if isinstance(self.related_devices, list) else [],
            'autoAdjust': self.auto_adjust,
            'tempThreshold': self.temp_threshold,
            'oxygenThreshold': self.oxygen_threshold,
            'phThreshold': self.ph_threshold
        }
    
    def __repr__(self):
        return f'<DeviceLinkageConfig {self.id}>'
