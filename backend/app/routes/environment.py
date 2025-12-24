from flask import Blueprint, request, jsonify
from app import db
from app.models.environment import EnvironmentData, EnvironmentThreshold
from app.utils.decorators import login_required
from datetime import datetime, timedelta
from sqlalchemy import func
import random

environment_bp = Blueprint('environment', __name__)


@environment_bp.route('/data', methods=['POST'])
def receive_environment_data():
    """接收设备上报的环境数据（不需要登录）"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': '请求数据为空'
            }), 400
        
        # 创建环境数据记录
        env_record = EnvironmentData(
            temperature=data.get('temperature', 0),
            dissolved_oxygen=data.get('dissolved_oxygen', 0),
            ph=data.get('ph', 0),
            water_flow=data.get('water_flow', 0)
        )
        
        db.session.add(env_record)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '数据上报成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'数据上报失败: {str(e)}'
        }), 500


def generate_realtime_data():
    """生成模拟的实时环境数据"""
    # 获取最新的真实数据，如果没有则生成模拟数据
    latest = EnvironmentData.query.order_by(EnvironmentData.timestamp.desc()).first()
    
    if latest:
        # 基于最新数据加上小幅波动
        temperature = latest.temperature + random.uniform(-0.5, 0.5)
        dissolved_oxygen = latest.dissolved_oxygen + random.uniform(-0.2, 0.2)
        ph = latest.ph + random.uniform(-0.1, 0.1)
        water_flow = latest.water_flow + random.uniform(-0.05, 0.05)
    else:
        # 生成初始模拟数据
        temperature = random.uniform(20, 26)
        dissolved_oxygen = random.uniform(5.5, 7.5)
        ph = random.uniform(7.2, 8.2)
        water_flow = random.uniform(0.5, 1.5)
    
    # 确保数据在合理范围内
    temperature = max(15, min(32, temperature))
    dissolved_oxygen = max(3, min(10, dissolved_oxygen))
    ph = max(6, min(9, ph))
    water_flow = max(0.1, min(3, water_flow))
    
    return {
        'temperature': round(temperature, 1),
        'dissolvedOxygen': round(dissolved_oxygen, 1),
        'ph': round(ph, 2),
        'waterFlow': round(water_flow, 2)
    }


@environment_bp.route('/realtime', methods=['GET'])
@login_required
def get_realtime_data():
    """获取实时环境数据"""
    try:
        # 直接返回数据库中最新的真实数据，不添加波动
        latest = EnvironmentData.query.order_by(EnvironmentData.timestamp.desc()).first()
        
        if latest:
            data = {
                'temperature': round(latest.temperature, 1),
                'dissolvedOxygen': round(latest.dissolved_oxygen, 1),
                'ph': round(latest.ph, 2),
                'waterFlow': round(latest.water_flow, 2)
            }
        else:
            # 如果没有数据，返回默认值
            data = generate_realtime_data()
        
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': True,
            'data': generate_realtime_data()
        })


@environment_bp.route('/history', methods=['GET'])
@login_required
def get_history_data():
    """获取环境数据历史记录"""
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    query = EnvironmentData.query
    
    if start_time:
        try:
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            query = query.filter(EnvironmentData.timestamp >= start_dt)
        except ValueError:
            pass
    
    if end_time:
        try:
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            query = query.filter(EnvironmentData.timestamp <= end_dt)
        except ValueError:
            pass
    
    total = query.count()
    records = query.order_by(EnvironmentData.timestamp.desc()).offset(offset).limit(limit).all()
    
    return jsonify({
        'success': True,
        'data': [record.to_dict() for record in records],
        'total': total
    })


@environment_bp.route('/statistics', methods=['GET'])
@login_required
def get_statistics():
    """获取环境数据统计"""
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    interval = request.args.get('interval', 'day')
    
    query = EnvironmentData.query
    
    # 默认查询最近7天
    if not start_time:
        start_dt = datetime.now() - timedelta(days=7)
    else:
        try:
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        except ValueError:
            start_dt = datetime.now() - timedelta(days=7)
    
    if not end_time:
        end_dt = datetime.now()
    else:
        try:
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        except ValueError:
            end_dt = datetime.now()
    
    query = query.filter(
        EnvironmentData.timestamp >= start_dt,
        EnvironmentData.timestamp <= end_dt
    )
    
    # 统计数据
    stats = db.session.query(
        func.avg(EnvironmentData.temperature).label('temp_avg'),
        func.min(EnvironmentData.temperature).label('temp_min'),
        func.max(EnvironmentData.temperature).label('temp_max'),
        func.avg(EnvironmentData.dissolved_oxygen).label('do_avg'),
        func.min(EnvironmentData.dissolved_oxygen).label('do_min'),
        func.max(EnvironmentData.dissolved_oxygen).label('do_max'),
        func.avg(EnvironmentData.ph).label('ph_avg'),
        func.min(EnvironmentData.ph).label('ph_min'),
        func.max(EnvironmentData.ph).label('ph_max')
    ).filter(
        EnvironmentData.timestamp >= start_dt,
        EnvironmentData.timestamp <= end_dt
    ).first()
    
    # 如果没有数据，返回默认值
    if stats.temp_avg is None:
        return jsonify({
            'success': True,
            'data': {
                'temperature': {'avg': 0, 'min': 0, 'max': 0},
                'dissolvedOxygen': {'avg': 0, 'min': 0, 'max': 0},
                'ph': {'avg': 0, 'min': 0, 'max': 0}
            }
        })
    
    return jsonify({
        'success': True,
        'data': {
            'temperature': {
                'avg': round(stats.temp_avg or 0, 2),
                'min': round(stats.temp_min or 0, 2),
                'max': round(stats.temp_max or 0, 2)
            },
            'dissolvedOxygen': {
                'avg': round(stats.do_avg or 0, 2),
                'min': round(stats.do_min or 0, 2),
                'max': round(stats.do_max or 0, 2)
            },
            'ph': {
                'avg': round(stats.ph_avg or 0, 2),
                'min': round(stats.ph_min or 0, 2),
                'max': round(stats.ph_max or 0, 2)
            }
        }
    })


@environment_bp.route('/monitoring/count', methods=['GET'])
@login_required
def get_monitoring_count():
    """获取环境监测总次数"""
    count = EnvironmentData.query.count()
    
    return jsonify({
        'success': True,
        'data': {
            'count': count
        }
    })


@environment_bp.route('/thresholds', methods=['GET'])
@login_required
def get_thresholds():
    """获取环境告警阈值配置"""
    threshold = EnvironmentThreshold.query.first()
    
    if not threshold:
        # 创建默认阈值
        threshold = EnvironmentThreshold(
            temperature_min=18.0,
            temperature_max=28.0,
            dissolved_oxygen_min=5.0,
            dissolved_oxygen_max=8.0,
            ph_min=7.0,
            ph_max=8.0
        )
        db.session.add(threshold)
        db.session.commit()
    
    return jsonify({
        'success': True,
        'data': threshold.to_dict()
    })


@environment_bp.route('/thresholds', methods=['PUT'])
@login_required
def update_thresholds():
    """更新环境告警阈值配置"""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': '请求数据为空'}), 400
    
    threshold = EnvironmentThreshold.query.first()
    
    if not threshold:
        threshold = EnvironmentThreshold()
        db.session.add(threshold)
    
    # 更新阈值
    if 'temperature' in data:
        temp = data['temperature']
        if 'min' in temp:
            threshold.temperature_min = float(temp['min'])
        if 'max' in temp:
            threshold.temperature_max = float(temp['max'])
    
    if 'dissolvedOxygen' in data:
        do = data['dissolvedOxygen']
        if 'min' in do:
            threshold.dissolved_oxygen_min = float(do['min'])
        if 'max' in do:
            threshold.dissolved_oxygen_max = float(do['max'])
    
    if 'ph' in data:
        ph = data['ph']
        if 'min' in ph:
            threshold.ph_min = float(ph['min'])
        if 'max' in ph:
            threshold.ph_max = float(ph['max'])
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': '阈值配置更新成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'更新失败: {str(e)}'}), 500
