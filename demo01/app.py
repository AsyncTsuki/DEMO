from flask import Flask,request,render_template

app = Flask(__name__)

class User:
    def __init__(self,username,email):
        self.username=username
        self.email=email

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
