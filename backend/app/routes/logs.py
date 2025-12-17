from flask import Blueprint, request, jsonify
from app import db
from app.models.log import Log
from app.utils.decorators import login_required
from datetime import datetime, timedelta
from sqlalchemy import or_

logs_bp = Blueprint('logs', __name__)


@logs_bp.route('', methods=['GET'])
@login_required
def get_logs():
    """获取系统日志列表"""
    level = request.args.get('level')
    module = request.args.get('module')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    query = Log.query
    
    if level:
        query = query.filter(Log.level == level)
    
    if module:
        query = query.filter(Log.module == module)
    
    if start_time:
        try:
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            query = query.filter(Log.timestamp >= start_dt)
        except ValueError:
            pass
    
    if end_time:
        try:
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            query = query.filter(Log.timestamp <= end_dt)
        except ValueError:
            pass
    
    # 分页
    logs = query.order_by(Log.timestamp.desc()).offset((page - 1) * per_page).limit(per_page).all()
    total = query.count()
    
    return jsonify({
        'success': True,
        'data': [log.to_dict() for log in logs],
        'total': total,
        'page': page,
        'per_page': per_page
    })


@logs_bp.route('/<int:log_id>', methods=['GET'])
@login_required
def get_log_detail(log_id):
    """获取单个日志详情"""
    log = Log.query.get(log_id)
    
    if not log:
        return jsonify({'success': False, 'message': '日志不存在'}), 404
    
    return jsonify({
        'success': True,
        'data': log.to_dict()
    })


@logs_bp.route('/search', methods=['GET'])
@login_required
def search_logs():
    """搜索日志"""
    keyword = request.args.get('keyword', '')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    query = Log.query
    
    if keyword:
        search_pattern = f'%{keyword}%'
        query = query.filter(
            or_(
                Log.action.like(search_pattern),
                Log.details.like(search_pattern),
                Log.operator.like(search_pattern),
                Log.module.like(search_pattern)
            )
        )
    
    if start_time:
        try:
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            query = query.filter(Log.timestamp >= start_dt)
        except ValueError:
            pass
    
    if end_time:
        try:
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            query = query.filter(Log.timestamp <= end_dt)
        except ValueError:
            pass
    
    logs = query.order_by(Log.timestamp.desc()).offset((page - 1) * per_page).limit(per_page).all()
    total = query.count()
    
    return jsonify({
        'success': True,
        'data': [log.to_dict() for log in logs],
        'total': total
    })


@logs_bp.route('/statistics', methods=['GET'])
@login_required
def get_log_statistics():
    """获取日志统计数据"""
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    
    query = Log.query
    
    # 默认查询最近30天
    if not start_time:
        start_dt = datetime.now() - timedelta(days=30)
    else:
        try:
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        except ValueError:
            start_dt = datetime.now() - timedelta(days=30)
    
    if not end_time:
        end_dt = datetime.now()
    else:
        try:
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        except ValueError:
            end_dt = datetime.now()
    
    query = query.filter(
        Log.timestamp >= start_dt,
        Log.timestamp <= end_dt
    )
    
    total = query.count()
    info_count = query.filter(Log.level == 'INFO').count()
    warning_count = query.filter(Log.level == 'WARNING').count()
    error_count = query.filter(Log.level == 'ERROR').count()
    
    return jsonify({
        'success': True,
        'data': {
            'info': info_count,
            'warning': warning_count,
            'error': error_count,
            'total': total
        }
    })
