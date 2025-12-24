from flask import Blueprint, request, jsonify, session
from app import db
from app.models.device import Device, DeviceConfig, DeviceLinkageConfig
from app.models.log import Log
from app.utils.decorators import login_required, get_current_username, get_client_ip
from app.utils.validators import validate_required, sanitize_string, validate_in_list
from datetime import datetime

devices_bp = Blueprint('devices', __name__)


@devices_bp.route('', methods=['GET'])
@login_required
def get_devices():
    """获取设备列表"""
    device_type = request.args.get('type')
    status = request.args.get('status')
    
    query = Device.query
    
    if device_type:
        query = query.filter(Device.type == device_type)
    
    if status:
        query = query.filter(Device.status == status)
    
    devices = query.order_by(Device.created_at.desc()).all()
    
    return jsonify({
        'success': True,
        'data': [device.to_dict() for device in devices]
    })


@devices_bp.route('/<device_id>', methods=['GET'])
@login_required
def get_device(device_id):
    """获取单个设备信息"""
    device = Device.query.get(device_id)
    
    if not device:
        return jsonify({'success': False, 'message': '设备不存在'}), 404
    
    return jsonify({
        'success': True,
        'data': device.to_dict()
    })


@devices_bp.route('/<device_id>/status', methods=['PATCH'])
def update_device_status(device_id):
    """更新设备状态"""
    device = Device.query.get(device_id)
    
    if not device:
        return jsonify({'success': False, 'message': '设备不存在'}), 404
    
    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({'success': False, 'message': '缺少status参数'}), 400
    
    new_status = data['status']
    valid, msg = validate_in_list(new_status, ['online', 'offline'], '状态')
    if not valid:
        return jsonify({'success': False, 'message': msg}), 400
    
    old_status = device.status
    device.status = new_status
    
    try:
        db.session.commit()
        
        # 记录日志
        log = Log(
            level='INFO',
            module='设备管理',
            operator=get_current_username() or 'system',
            action='更新设备状态',
            details=f'设备 {device.name}({device_id}) 状态从 {old_status} 更新为 {new_status}',
            ip=get_client_ip()
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '设备状态更新成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'更新失败: {str(e)}'}), 500


@devices_bp.route('/<device_id>/config', methods=['GET'])
@login_required
def get_device_config(device_id):
    """获取设备配置"""
    device = Device.query.get(device_id)
    
    if not device:
        return jsonify({'success': False, 'message': '设备不存在'}), 404
    
    config = DeviceConfig.query.filter_by(device_id=device_id).first()
    
    if not config:
        return jsonify({
            'success': True,
            'data': {'config': {}}
        })
    
    return jsonify({
        'success': True,
        'data': {'config': config.config}
    })


@devices_bp.route('/<device_id>/config', methods=['PUT'])
@login_required
def save_device_config(device_id):
    """保存设备配置"""
    device = Device.query.get(device_id)
    
    if not device:
        return jsonify({'success': False, 'message': '设备不存在'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '请求数据为空'}), 400
    
    config = DeviceConfig.query.filter_by(device_id=device_id).first()
    
    if not config:
        config = DeviceConfig(device_id=device_id, config=data)
        db.session.add(config)
    else:
        config.config = data
    
    try:
        db.session.commit()
        
        # 记录日志
        log = Log(
            level='INFO',
            module='设备管理',
            operator=get_current_username() or 'system',
            action='更新设备配置',
            details=f'设备 {device.name}({device_id}) 配置已更新',
            ip=get_client_ip()
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '设备配置保存成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'保存失败: {str(e)}'}), 500


@devices_bp.route('/linkage', methods=['GET'])
@login_required
def get_linkage_config():
    """获取设备联动配置"""
    config = DeviceLinkageConfig.query.first()
    
    if not config:
        # 返回默认配置
        return jsonify({
            'success': True,
            'data': {
                'triggerType': 'time',
                'interval': 60,
                'relatedDevices': [],
                'autoAdjust': False,
                'tempThreshold': 25.0,
                'oxygenThreshold': 6.0,
                'phThreshold': 7.5
            }
        })
    
    return jsonify({
        'success': True,
        'data': config.to_dict()
    })


@devices_bp.route('/linkage', methods=['PUT'])
@login_required
def save_linkage_config():
    """保存设备联动配置"""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': '请求数据为空'}), 400
    
    config = DeviceLinkageConfig.query.first()
    
    if not config:
        config = DeviceLinkageConfig()
        db.session.add(config)
    
    # 更新配置
    if 'triggerType' in data:
        config.trigger_type = data['triggerType']
    if 'interval' in data:
        config.interval = int(data['interval'])
    if 'relatedDevices' in data:
        config.related_devices = data['relatedDevices']
    if 'autoAdjust' in data:
        config.auto_adjust = bool(data['autoAdjust'])
    if 'tempThreshold' in data:
        config.temp_threshold = float(data['tempThreshold'])
    if 'oxygenThreshold' in data:
        config.oxygen_threshold = float(data['oxygenThreshold'])
    if 'phThreshold' in data:
        config.ph_threshold = float(data['phThreshold'])
    
    try:
        db.session.commit()
        
        # 记录日志
        log = Log(
            level='INFO',
            module='设备管理',
            operator=get_current_username() or 'system',
            action='更新设备联动配置',
            details='设备联动配置已更新',
            ip=get_client_ip()
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '设备联动配置保存成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'保存失败: {str(e)}'}), 500
