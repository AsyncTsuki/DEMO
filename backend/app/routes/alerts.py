from flask import Blueprint, request, jsonify
from app import db
from app.models.alert import Alert, AlertNotificationSetting
from app.models.log import Log
from app.utils.decorators import login_required, get_current_username, get_current_user_id, get_client_ip
from datetime import datetime
from sqlalchemy import func

alerts_bp = Blueprint('alerts', __name__)


@alerts_bp.route('', methods=['GET'])
@login_required
def get_alerts():
    """获取告警列表"""
    level = request.args.get('level')
    resolved = request.args.get('resolved')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    
    query = Alert.query
    
    if level:
        query = query.filter(Alert.level == level)
    
    if resolved is not None:
        resolved_bool = resolved.lower() in ('true', '1', 'yes')
        query = query.filter(Alert.resolved == resolved_bool)
    
    if start_time:
        try:
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            query = query.filter(Alert.time >= start_dt)
        except ValueError:
            pass
    
    if end_time:
        try:
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            query = query.filter(Alert.time <= end_dt)
        except ValueError:
            pass
    
    alerts = query.order_by(Alert.time.desc()).limit(200).all()
    
    return jsonify({
        'success': True,
        'data': [alert.to_dict() for alert in alerts]
    })


@alerts_bp.route('/<int:alert_id>', methods=['GET'])
@login_required
def get_alert_detail(alert_id):
    """获取单个告警详情"""
    alert = Alert.query.get(alert_id)
    
    if not alert:
        return jsonify({'success': False, 'message': '告警不存在'}), 404
    
    return jsonify({
        'success': True,
        'data': alert.to_dict()
    })


@alerts_bp.route('/<int:alert_id>/resolve', methods=['PATCH'])
@login_required
def resolve_alert(alert_id):
    """标记告警为已处理"""
    alert = Alert.query.get(alert_id)
    
    if not alert:
        return jsonify({'success': False, 'message': '告警不存在'}), 404
    
    if alert.resolved:
        return jsonify({'success': False, 'message': '告警已被处理'}), 400
    
    try:
        username = get_current_username() or 'system'
        alert.resolved = True
        alert.resolved_at = datetime.now()
        alert.resolved_by = username
        
        db.session.commit()
        
        # 记录日志
        log = Log(
            level='INFO',
            module='告警管理',
            operator=username,
            action='处理告警',
            details=f'处理告警: {alert.title} (ID: {alert_id})',
            ip=get_client_ip()
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '告警已标记为已处理'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'处理失败: {str(e)}'}), 500


@alerts_bp.route('/statistics', methods=['GET'])
@login_required
def get_alert_statistics():
    """获取告警统计数据"""
    total = Alert.query.count()
    warning_count = Alert.query.filter(Alert.level == 'warning').count()
    error_count = Alert.query.filter(Alert.level == 'error').count()
    resolved_count = Alert.query.filter(Alert.resolved == True).count()
    
    return jsonify({
        'success': True,
        'data': {
            'total': total,
            'warning': warning_count,
            'error': error_count,
            'resolved': resolved_count
        }
    })


@alerts_bp.route('/unresolved/count', methods=['GET'])
@login_required
def get_unresolved_count():
    """获取未处理的告警数量"""
    count = Alert.query.filter(Alert.resolved == False).count()
    
    return jsonify({
        'success': True,
        'data': {
            'count': count
        }
    })


@alerts_bp.route('/notifications', methods=['GET'])
@login_required
def get_notification_settings():
    """获取告警通知设置"""
    user_id = get_current_user_id()
    setting = AlertNotificationSetting.query.filter_by(user_id=user_id).first()
    
    if not setting:
        return jsonify({
            'success': True,
            'data': {
                'email': True,
                'sms': False,
                'push': True
            }
        })
    
    return jsonify({
        'success': True,
        'data': setting.to_dict()
    })


@alerts_bp.route('/notifications', methods=['PUT'])
@login_required
def update_notification_settings():
    """配置告警通知设置"""
    user_id = get_current_user_id()
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': '请求数据为空'}), 400
    
    setting = AlertNotificationSetting.query.filter_by(user_id=user_id).first()
    
    if not setting:
        setting = AlertNotificationSetting(user_id=user_id)
        db.session.add(setting)
    
    if 'email' in data:
        setting.email = bool(data['email'])
    if 'sms' in data:
        setting.sms = bool(data['sms'])
    if 'push' in data:
        setting.push = bool(data['push'])
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': '告警通知设置更新成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'更新失败: {str(e)}'}), 500
