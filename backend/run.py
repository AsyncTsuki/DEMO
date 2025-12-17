from app import create_app, db

app = create_app('development')

if __name__ == '__main__':
    with app.app_context():
        # 创建所有数据库表
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
