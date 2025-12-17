from functools import wraps
from flask import session, request, jsonify


def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({
                'success': False,
                'message': '未授权访问，请先登录',
                'code': 401
            }), 401
        return f(*args, **kwargs)
    return decorated_function


def get_current_user_id():
    """获取当前登录用户ID"""
    return session.get('user_id')


def get_current_username():
    """获取当前登录用户名"""
    return session.get('username')


def get_client_ip():
    """获取客户端IP地址"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr or '127.0.0.1'
