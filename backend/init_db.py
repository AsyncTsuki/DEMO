"""
数据库初始化脚本

运行此脚本将创建数据库表并插入初始数据
使用方法: python init_db.py
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import (
    User, EnvironmentData, EnvironmentThreshold, 
    Device, DeviceConfig, DeviceLinkageConfig,
    FeedingPlan, FeedingHistory, Alert, Log, Pond
)
from datetime import datetime, timedelta, time
import random


def init_database():
    """初始化数据库"""
    app = create_app('development')
    
    with app.app_context():
        print("开始创建数据库表...")
        db.create_all()
        print("数据库表创建完成！")
        
        # 检查是否已有数据（检查设备数据）
        if Device.query.first():
            print("数据库已包含设备数据，跳过初始化...")
            return
        
        print("开始插入初始数据...")
        
        # 创建测试用户
        admin_user = User(username='admin', email='admin@fishery.com')
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        
        test_user = User(username='test', email='test@fishery.com')
        test_user.set_password('test123')
        db.session.add(test_user)
        
        # 创建环境阈值
        threshold = EnvironmentThreshold(
            temperature_min=18.0,
            temperature_max=28.0,
            dissolved_oxygen_min=5.0,
            dissolved_oxygen_max=8.0,
            ph_min=7.0,
            ph_max=8.0
        )
        db.session.add(threshold)
        
        # 创建设备
        devices = [
            Device(id='feeder-001', name='智能投喂机1号', type='feeder', status='online', location='A区1号网箱'),
            Device(id='feeder-002', name='智能投喂机2号', type='feeder', status='online', location='A区2号网箱'),
            Device(id='feeder-003', name='智能投喂机3号', type='feeder', status='offline', location='B区1号网箱'),
            Device(id='sensor-001', name='水质传感器1号', type='sensor', status='online', location='A区监测点'),
            Device(id='sensor-002', name='水质传感器2号', type='sensor', status='online', location='B区监测点'),
            Device(id='camera-001', name='水下摄像头1号', type='camera', status='online', location='A区1号网箱'),
        ]
        for device in devices:
            db.session.add(device)
        
        db.session.commit()
        
        # 创建鱼塘数据
        now = datetime.now()  # 定义now变量
        fish_types = ['大黄鱼', '鲈鱼', '石斑鱼', '对虾', '海参']
        locations = ['A区', 'B区', 'C区', 'D区']
        ponds = []
        
        # 创建25个鱼塘（分布在过去12个月）
        for i in range(25):
            # 让鱼塘创建时间分布在过去12个月
            months_ago = 11 - (i // 2)
            created_date = now - timedelta(days=months_ago * 30 + random.randint(0, 20))
            
            pond = Pond(
                name=f'{random.choice(locations)}{i + 1}号鱼塘',
                location=f'{random.choice(locations)}养殖区{random.randint(1, 10)}号位',
                area=round(random.uniform(800, 2000), 1),
                depth=round(random.uniform(2.5, 5.0), 1),
                capacity=random.randint(50000, 200000),
                fish_type=random.choice(fish_types),
                fish_count=random.randint(40000, 180000),
                status='active' if random.random() > 0.1 else 'maintenance',
                created_at=created_date,
                updated_at=created_date,
                notes=f'养殖周期 {random.randint(3, 8)} 个月'
            )
            ponds.append(pond)
            db.session.add(pond)
        
        db.session.commit()
        
        # 创建设备联动配置
        linkage_config = DeviceLinkageConfig(
            trigger_type='environment',
            interval=30,
            related_devices=['feeder-001', 'feeder-002', 'sensor-001'],
            auto_adjust=True,
            temp_threshold=25.0,
            oxygen_threshold=6.0,
            ph_threshold=7.5
        )
        db.session.add(linkage_config)
        
        # 创建投喂计划
        feeding_plans = [
            FeedingPlan(name='早间投喂', device_id='feeder-001', time=time(7, 0), amount=50.0, status='active'),
            FeedingPlan(name='午间投喂', device_id='feeder-001', time=time(12, 0), amount=45.0, status='active'),
            FeedingPlan(name='晚间投喂', device_id='feeder-001', time=time(18, 0), amount=55.0, status='active'),
            FeedingPlan(name='早间投喂', device_id='feeder-002', time=time(7, 30), amount=48.0, status='active'),
            FeedingPlan(name='午间投喂', device_id='feeder-002', time=time(12, 30), amount=42.0, status='active'),
        ]
        for plan in feeding_plans:
            db.session.add(plan)
        
        # 创建历史环境数据（最近7天）
        now = datetime.now()
        for i in range(7 * 24):  # 7天，每小时一条
            timestamp = now - timedelta(hours=i)
            env_data = EnvironmentData(
                timestamp=timestamp,
                temperature=round(random.uniform(20, 26), 1),
                dissolved_oxygen=round(random.uniform(5.5, 7.5), 1),
                ph=round(random.uniform(7.2, 8.2), 2),
                water_flow=round(random.uniform(0.5, 1.5), 2)
            )
            db.session.add(env_data)
        
        # 创建投喂历史
        fish_types = ['大黄鱼', '鲈鱼', '石斑鱼', '对虾', '海参']
        for i in range(50):  # 50条历史记录
            timestamp = now - timedelta(days=i // 2, hours=random.randint(6, 18))
            history = FeedingHistory(
                device_id=random.choice(['feeder-001', 'feeder-002']),
                amount=round(random.uniform(40, 60), 1),
                time=timestamp,
                timestamp=timestamp,  # 添加timestamp字段
                type=random.choice(['auto', 'manual']),
                operator='system' if random.random() > 0.3 else 'admin',
                fish_type=random.choice(fish_types),  # 添加鱼种
                fish_count=random.randint(80000, 200000),  # 添加鱼群数量
                average_weight=round(random.uniform(300, 800), 1)  # 添加平均体重
            )
            db.session.add(history)
        
        # 创建告警
        alerts_data = [
            {'title': '水温异常警告', 'level': 'warning', 'location': 'A区1号网箱', 'description': '水温达到27.5°C，接近上限', 'resolved': True},
            {'title': '溶解氧过低', 'level': 'error', 'location': 'B区1号网箱', 'description': '溶解氧降至4.2mg/L，低于安全值', 'resolved': True},
            {'title': 'pH值异常', 'level': 'warning', 'location': 'A区监测点', 'description': 'pH值达到8.5，略高于正常范围', 'resolved': False},
            {'title': '投喂设备故障', 'level': 'error', 'location': 'B区1号网箱', 'description': '投喂机3号通信异常，请检查设备', 'resolved': False},
            {'title': '水流速度异常', 'level': 'warning', 'location': 'A区2号网箱', 'description': '水流速度降低，可能影响水质', 'resolved': True},
        ]
        for i, alert_data in enumerate(alerts_data):
            alert = Alert(
                title=alert_data['title'],
                level=alert_data['level'],
                location=alert_data['location'],
                description=alert_data['description'],
                resolved=alert_data['resolved'],
                time=now - timedelta(days=i, hours=random.randint(0, 12))
            )
            if alert.resolved:
                alert.resolved_at = alert.time + timedelta(hours=random.randint(1, 5))
                alert.resolved_by = 'admin'
            db.session.add(alert)
        
        # 创建系统日志
        log_actions = [
            ('INFO', '认证', '用户登录', '用户 admin 登录成功'),
            ('INFO', '投喂管理', '执行投喂', '设备 feeder-001 执行自动投喂 50kg'),
            ('WARNING', '环境监测', '阈值警告', '水温接近上限阈值'),
            ('INFO', '设备管理', '设备上线', '设备 feeder-001 已上线'),
            ('ERROR', '设备管理', '设备故障', '设备 feeder-003 通信中断'),
        ]
        for i in range(20):
            action = random.choice(log_actions)
            log = Log(
                level=action[0],
                module=action[1],
                action=action[2],
                details=action[3],
                operator='admin',
                ip='127.0.0.1',
                timestamp=now - timedelta(hours=i * 2)
            )
            db.session.add(log)
        
        db.session.commit()
        print("初始数据插入完成！")
        print("\n测试账户信息:")
        print("  用户名: admin  密码: admin123")
        print("  用户名: test   密码: test123")


if __name__ == '__main__':
    init_database()
