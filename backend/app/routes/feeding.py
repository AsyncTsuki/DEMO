from flask import Blueprint, request, jsonify
from app import db
from app.models.feeding import FeedingPlan, FeedingHistory
from app.models.device import Device
from app.models.environment import EnvironmentData
from app.models.log import Log
from app.utils.decorators import login_required, get_current_username, get_client_ip
from app.utils.validators import (
    validate_required, validate_positive_number, 
    validate_time_format, validate_in_list, sanitize_string
)
from app.services.feeding_algorithm import calculate_feeding
from datetime import datetime, time as time_type

feeding_bp = Blueprint('feeding', __name__)


@feeding_bp.route('/plans', methods=['GET'])
@login_required
def get_feeding_plans():
    """获取投喂计划列表"""
    device_id = request.args.get('device_id')
    status = request.args.get('status')
    
    query = FeedingPlan.query
    
    if device_id:
        query = query.filter(FeedingPlan.device_id == device_id)
    
    if status:
        query = query.filter(FeedingPlan.status == status)
    
    plans = query.order_by(FeedingPlan.created_at.desc()).all()
    
    return jsonify({
        'success': True,
        'data': [plan.to_dict() for plan in plans]
    })


@feeding_bp.route('/plans', methods=['POST'])
@login_required
def create_feeding_plan():
    """创建投喂计划"""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': '请求数据为空'}), 400
    
    # 验证必填字段
    error = validate_required(data, ['name', 'device_id', 'time', 'amount'])
    if error:
        return jsonify({'success': False, 'message': error}), 400
    
    # 验证设备是否存在
    device_id = data['device_id']
    device = Device.query.get(device_id)
    if not device:
        return jsonify({'success': False, 'message': '设备不存在'}), 404
    
    # 验证时间格式
    time_str = data['time']
    valid, msg = validate_time_format(time_str)
    if not valid:
        return jsonify({'success': False, 'message': msg}), 400
    
    # 验证投喂量
    valid, msg = validate_positive_number(data['amount'], '投喂量')
    if not valid:
        return jsonify({'success': False, 'message': msg}), 400
    
    # 验证状态
    status = data.get('status', 'active')
    valid, msg = validate_in_list(status, ['active', 'inactive'], '状态')
    if not valid:
        return jsonify({'success': False, 'message': msg}), 400
    
    try:
        # 解析时间
        hour, minute = map(int, time_str.split(':'))
        plan_time = time_type(hour, minute)
        
        plan = FeedingPlan(
            name=sanitize_string(data['name']),
            device_id=device_id,
            time=plan_time,
            amount=float(data['amount']),
            status=status
        )
        db.session.add(plan)
        db.session.commit()
        
        # 记录日志
        log = Log(
            level='INFO',
            module='投喂管理',
            operator=get_current_username() or 'system',
            action='创建投喂计划',
            details=f'创建投喂计划: {plan.name}, 设备: {device_id}, 时间: {time_str}, 投喂量: {plan.amount}kg',
            ip=get_client_ip()
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '投喂计划创建成功', 'data': plan.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'创建失败: {str(e)}'}), 500


@feeding_bp.route('/plans/<int:plan_id>', methods=['PUT'])
@login_required
def update_feeding_plan(plan_id):
    """更新投喂计划"""
    plan = FeedingPlan.query.get(plan_id)
    
    if not plan:
        return jsonify({'success': False, 'message': '投喂计划不存在'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '请求数据为空'}), 400
    
    try:
        if 'name' in data:
            plan.name = sanitize_string(data['name'])
        
        if 'device_id' in data:
            device = Device.query.get(data['device_id'])
            if not device:
                return jsonify({'success': False, 'message': '设备不存在'}), 404
            plan.device_id = data['device_id']
        
        if 'time' in data:
            valid, msg = validate_time_format(data['time'])
            if not valid:
                return jsonify({'success': False, 'message': msg}), 400
            hour, minute = map(int, data['time'].split(':'))
            plan.time = time_type(hour, minute)
        
        if 'amount' in data:
            valid, msg = validate_positive_number(data['amount'], '投喂量')
            if not valid:
                return jsonify({'success': False, 'message': msg}), 400
            plan.amount = float(data['amount'])
        
        if 'status' in data:
            valid, msg = validate_in_list(data['status'], ['active', 'inactive'], '状态')
            if not valid:
                return jsonify({'success': False, 'message': msg}), 400
            plan.status = data['status']
        
        db.session.commit()
        
        # 记录日志
        log = Log(
            level='INFO',
            module='投喂管理',
            operator=get_current_username() or 'system',
            action='更新投喂计划',
            details=f'更新投喂计划ID: {plan_id}',
            ip=get_client_ip()
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '投喂计划更新成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'更新失败: {str(e)}'}), 500


@feeding_bp.route('/plans/<int:plan_id>', methods=['DELETE'])
@login_required
def delete_feeding_plan(plan_id):
    """删除投喂计划"""
    plan = FeedingPlan.query.get(plan_id)
    
    if not plan:
        return jsonify({'success': False, 'message': '投喂计划不存在'}), 404
    
    try:
        plan_name = plan.name
        db.session.delete(plan)
        db.session.commit()
        
        # 记录日志
        log = Log(
            level='INFO',
            module='投喂管理',
            operator=get_current_username() or 'system',
            action='删除投喂计划',
            details=f'删除投喂计划: {plan_name} (ID: {plan_id})',
            ip=get_client_ip()
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '投喂计划删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'删除失败: {str(e)}'}), 500


@feeding_bp.route('/execute', methods=['POST'])
@login_required
def execute_manual_feeding():
    """执行手动投喂"""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': '请求数据为空'}), 400
    
    # 验证必填字段
    error = validate_required(data, ['deviceId', 'amount'])
    if error:
        return jsonify({'success': False, 'message': error}), 400
    
    device_id = data['deviceId']
    device = Device.query.get(device_id)
    
    if not device:
        return jsonify({'success': False, 'message': '设备不存在'}), 404
    
    # 验证投喂量
    valid, msg = validate_positive_number(data['amount'], '投喂量')
    if not valid:
        return jsonify({'success': False, 'message': msg}), 400
    
    try:
        # 记录投喂历史
        history = FeedingHistory(
            device_id=device_id,
            amount=float(data['amount']),
            type='manual',
            operator=get_current_username() or 'system'
        )
        db.session.add(history)
        db.session.commit()
        
        # 记录日志
        log = Log(
            level='INFO',
            module='投喂管理',
            operator=get_current_username() or 'system',
            action='执行手动投喂',
            details=f'设备: {device.name}({device_id}), 投喂量: {data["amount"]}kg',
            ip=get_client_ip()
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '投喂指令已发送'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'执行失败: {str(e)}'}), 500


@feeding_bp.route('/calculate', methods=['GET'])
@login_required
def calculate_feeding_amount():
    """计算建议投喂量"""
    fish_count = request.args.get('fishCount', type=int)
    average_weight = request.args.get('averageWeight', type=float)
    fish_type = request.args.get('fishType', 'default')
    
    if not fish_count or fish_count <= 0:
        return jsonify({'success': False, 'message': '鱼类数量必须大于0'}), 400
    
    if not average_weight or average_weight <= 0:
        return jsonify({'success': False, 'message': '平均体重必须大于0'}), 400
    
    # 获取最新环境数据
    latest_env = EnvironmentData.query.order_by(EnvironmentData.timestamp.desc()).first()
    
    env_data = {}
    if latest_env:
        env_data = {
            'temperature': latest_env.temperature,
            'dissolvedOxygen': latest_env.dissolved_oxygen,
            'ph': latest_env.ph
        }
    
    # 计算建议投喂量
    result = calculate_feeding(
        fish_count=fish_count,
        average_weight=average_weight,
        fish_type=fish_type,
        env_data=env_data
    )
    
    return jsonify({
        'success': True,
        'data': {
            'amount': result['amount'],
            'type': result['type'],
            'reason': result['reason']
        }
    })


@feeding_bp.route('/history', methods=['GET'])
@login_required
def get_feeding_history():
    """获取投喂历史记录"""
    device_id = request.args.get('device_id')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    
    query = FeedingHistory.query
    
    if device_id:
        query = query.filter(FeedingHistory.device_id == device_id)
    
    if start_time:
        try:
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            query = query.filter(FeedingHistory.time >= start_dt)
        except ValueError:
            pass
    
    if end_time:
        try:
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            query = query.filter(FeedingHistory.time <= end_dt)
        except ValueError:
            pass
    
    histories = query.order_by(FeedingHistory.time.desc()).limit(100).all()
    
    return jsonify({
        'success': True,
        'data': [history.to_dict() for history in histories]
    })


@feeding_bp.route('/statistics', methods=['GET'])
@login_required
def get_feeding_statistics():
    """获取投喂统计数据"""
    # 统计投喂记录总数
    total_feeding = FeedingHistory.query.count()
    
    # 统计投喂计划总数
    total_plans = FeedingPlan.query.count()
    
    # 统计活跃的投喂计划数
    active_plans = FeedingPlan.query.filter(FeedingPlan.status == 'active').count()
    
    return jsonify({
        'success': True,
        'data': {
            'totalFeeding': total_feeding,
            'totalPlans': total_plans,
            'activePlans': active_plans
        }
    })
