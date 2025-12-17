from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import config

db = SQLAlchemy()


def create_app(config_name='default'):
    """应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    
    # 配置CORS，支持跨域携带cookie
    CORS(app, 
         origins=app.config['CORS_ORIGINS'],
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'])
    
    # 注册蓝图
    from app.routes.auth import auth_bp
    from app.routes.environment import environment_bp
    from app.routes.devices import devices_bp
    from app.routes.feeding import feeding_bp
    from app.routes.alerts import alerts_bp
    from app.routes.logs import logs_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(environment_bp, url_prefix='/api/environment')
    app.register_blueprint(devices_bp, url_prefix='/api/devices')
    app.register_blueprint(feeding_bp, url_prefix='/api/feeding')
    app.register_blueprint(alerts_bp, url_prefix='/api/alerts')
    app.register_blueprint(logs_bp, url_prefix='/api/logs')
    
    # 注册错误处理
    register_error_handlers(app)
    
    return app


def register_error_handlers(app):
    """注册全局错误处理"""
    
    @app.errorhandler(400)
    def bad_request(e):
        return {'success': False, 'message': '请求参数错误', 'code': 400}, 400
    
    @app.errorhandler(401)
    def unauthorized(e):
        return {'success': False, 'message': '未授权访问', 'code': 401}, 401
    
    @app.errorhandler(403)
    def forbidden(e):
        return {'success': False, 'message': '权限不足', 'code': 403}, 403
    
    @app.errorhandler(404)
    def not_found(e):
        return {'success': False, 'message': '资源不存在', 'code': 404}, 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return {'success': False, 'message': '服务器内部错误', 'code': 500}, 500
