from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
app = Flask(__name__)

class User:
    def __init__(self,username,email):
        self.username=username
        self.email=email

HOSTNAME ="127.0.0.1"
PORT=3306
USERNAME ='root'
PASSWORD='plmokner123'
DATABASE='fishery'
app.config['SQLALCHEMY_DATABASE_URI']=f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"
db=SQLAlchemy(app)
with app.app_context():
    try:
        # 尝试连接数据库并执行查询
        with db.engine.connect() as conn:
            rs = conn.execute(text("select 1"))
            print("查询结果:", rs.fetchone())  # 应该输出 (1,)
    except Exception as e:
        # 捕获并打印所有可能的错误
        print("数据库操作出错:", str(e))
@app.route('/')
def hello_world():
    user=User("async","xx@qq.com")
    person={
        "username":"zhangsan",
        "email":"zhangsan@qq.com"
    }
    return render_template('index.html',user=user,person=person)

@app.route('/profile')
def profile():
    return "我是个人中心"

@app.route('/blog/<int:blog_id>')
def bolg_detail(blog_id):
    return render_template('blog_detail.html',blog_id=blog_id,username="async")

@app.route('/blog/list')
def blog_list():
    page = request.args.get('page', default=1, type=int)
    return f"您获取的是第{page}页的图书列表！"

if __name__ == '__main__':
    app.run()
