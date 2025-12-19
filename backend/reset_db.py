"""
数据库重置脚本 - 删除并重新创建数据库，包含测试数据

警告: 此脚本会删除所有现有数据！
使用方法: python reset_db.py
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db

def reset_database():
    """重置数据库"""
    app = create_app('development')
    
    with app.app_context():
        print("正在删除所有表...")
        db.drop_all()
        print("所有表已删除")
        
        print("正在重新创建表...")
        db.create_all()
        print("表创建完成")


if __name__ == '__main__':
    reset_database()
