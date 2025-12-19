from app import db
from datetime import datetime


class Pond(db.Model):
    """鱼塘表"""
    __tablename__ = 'ponds'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)  # 鱼塘名称
    location = db.Column(db.String(200), nullable=False)  # 位置
    area = db.Column(db.Float, nullable=False)  # 面积（平方米）
    depth = db.Column(db.Float, nullable=False)  # 深度（米）
    capacity = db.Column(db.Integer, nullable=False)  # 容量（尾）
    fish_type = db.Column(db.String(50))  # 养殖鱼种
    fish_count = db.Column(db.Integer, default=0)  # 当前鱼数量
    status = db.Column(db.String(20), nullable=False, default='active', index=True)  # active, inactive, maintenance
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    notes = db.Column(db.Text)  # 备注
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'area': self.area,
            'depth': self.depth,
            'capacity': self.capacity,
            'fishType': self.fish_type,
            'fishCount': self.fish_count,
            'status': self.status,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
            'notes': self.notes
        }
    
    def __repr__(self):
        return f'<Pond {self.name}>'
