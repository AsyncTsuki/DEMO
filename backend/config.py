import os
from datetime import timedelta

class Config:
    """基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fishery-smart-feeding-secret-key-2024'
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:root@localhost:3306/fishery?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Session配置 - 使用Flask内置的cookie-based session
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Cookie配置
    SESSION_COOKIE_NAME = 'fishery_session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # 生产环境设置为True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CORS配置
    CORS_ORIGINS = ['http://localhost:5173', 'http://127.0.0.1:5173', 'http://localhost:3000']


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
