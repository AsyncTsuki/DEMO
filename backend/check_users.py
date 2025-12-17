"""检查用户密码"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User

app = create_app('development')

with app.app_context():
    users = User.query.all()
    print(f"数据库中共有 {len(users)} 个用户:")
    for u in users:
        print(f"  用户名: {u.username}")
        print(f"    密码哈希: {u.password_hash[:60]}...")
        print(f"    验证 'admin123': {u.check_password('admin123')}")
        print(f"    验证 'test123': {u.check_password('test123')}")
        print()
