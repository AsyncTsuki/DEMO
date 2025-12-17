from flask import Blueprint, request, jsonify, session
from app import db
from app.models.user import User
from app.models.log import Log
from app.utils.decorators import login_required, get_current_user_id, get_client_ip
from app.utils.validators import (
    validate_required, validate_email, validate_username, 
    validate_password, sanitize_string
)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    
    # 调试输出
    print(f"[DEBUG] Login request data: {data}")
    
    if not data:
        return jsonify({'success': False, 'message': '请求数据为空'}), 400
    
    # 验证必填字段
    error = validate_required(data, ['username', 'password'])
    if error:
        return jsonify({'success': False, 'message': error}), 400
    
    username = sanitize_string(data.get('username', ''))
    password = data.get('password', '')
    
    print(f"[DEBUG] Username: {username}, Password length: {len(password)}")
    
    # 查找用户
    user = User.query.filter_by(username=username).first()
    
    print(f"[DEBUG] User found: {user is not None}")
    if user:
        print(f"[DEBUG] Password check: {user.check_password(password)}")
    
    if not user or not user.check_password(password):
        return jsonify({'success': False, 'message': '用户名或密码错误'}), 401
    
    # 设置session
    session['user_id'] = user.id
    session['username'] = user.username
    session.permanent = True
    
    # 记录登录日志
    try:
        log = Log(
            level='INFO',
            module='认证',
            operator=user.username,
            action='用户登录',
            details=f'用户 {user.username} 登录成功',
            ip=get_client_ip()
        )
        db.session.add(log)
        db.session.commit()
    except Exception:
        pass  # 日志记录失败不影响登录
    
    return jsonify({
        'success': True,
        'token': f'session_{user.id}',  # 使用session，这里返回一个标识
        'username': user.username,
        'user_id': user.id
    })


@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': '请求数据为空'}), 400
    
    # 验证必填字段
    error = validate_required(data, ['username', 'password', 'email'])
    if error:
        return jsonify({'success': False, 'message': error}), 400
    
    username = sanitize_string(data.get('username', ''))
    password = data.get('password', '')
    email = sanitize_string(data.get('email', ''))
    
    # 验证用户名
    valid, msg = validate_username(username)
    if not valid:
        return jsonify({'success': False, 'message': msg}), 400
    
    # 验证密码
    valid, msg = validate_password(password)
    if not valid:
        return jsonify({'success': False, 'message': msg}), 400
    
    # 验证邮箱
    if not validate_email(email):
        return jsonify({'success': False, 'message': '邮箱格式不正确'}), 400
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({'success': False, 'message': '用户名已存在'}), 400
    
    # 检查邮箱是否已存在
    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'message': '邮箱已被注册'}), 400
    
    try:
        # 创建用户
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        # 记录注册日志
        log = Log(
            level='INFO',
            module='认证',
            operator=username,
            action='用户注册',
            details=f'新用户 {username} 注册成功',
            ip=get_client_ip()
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '注册成功'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'注册失败: {str(e)}'}), 500


@auth_bp.route('/user', methods=['GET'])
@login_required
def get_current_user():
    """获取当前用户信息"""
    user_id = get_current_user_id()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'success': False, 'message': '用户不存在'}), 404
    
    return jsonify({
        'success': True,
        'user': user.to_dict()
    })


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """用户退出登录"""
    username = session.get('username', 'unknown')
    
    # 记录登出日志
    try:
        log = Log(
            level='INFO',
            module='认证',
            operator=username,
            action='用户登出',
            details=f'用户 {username} 退出登录',
            ip=get_client_ip()
        )
        db.session.add(log)
        db.session.commit()
    except Exception:
        pass
    
    # 清除session
    session.clear()
    
    return jsonify({'success': True, 'message': '退出成功'})
