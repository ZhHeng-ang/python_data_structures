import time
data_time=(time.strftime("%Y-%m-%d", time.localtime()))

from watchlist import app,db
from flask import request,redirect,url_for,flash,render_template
from flask_login import login_user,logout_user,login_required,current_user
from watchlist.models import User,Ariticles
# 首页
@app.route('/',methods=['GET','POST'])
def index():
    ariticles = Ariticles.query.all()
    return render_template('index.html',ariticles=ariticles)
# 编辑电影信息页面
@app.route('/ariticle/edit/<int:ariticles_id>',methods=['GET','POST'])
@login_required
def edit(ariticles_id):
    ariticle = Ariticles.query.get_or_404(ariticles_id)

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pubdate = request.form['pubdate']
        content = request.form['content']

        if not title or not author:
            flash('输入错误')
            return redirect(url_for('edit'),ariticles_id=ariticles_id)
        
        ariticle.title = title
        ariticle.author = author
        ariticle.pubdate = pubdate
        content_ = request.form.get('content')
        content_2 = content_.replace('<p>', '')
        content = content_2.replace('</p>', '')
        ariticle.content = content
        db.session.commit()
        flash('电影信息已经更新')
        return redirect(url_for('index'))
    return render_template('edit.html',ariticle=ariticle)

@app.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name)>20:
            flash('输入错误')
            return redirect(url_for('settings'))
        
        current_user.name = name
        db.session.commit()
        flash('设置name成功')
        return redirect(url_for('index'))

    return render_template('settings.html')

# 删除信息
@app.route('/ariticle/delete/<int:ariticles_id>',methods=['POST'])
@login_required    
def delete(ariticles_id):
    ariticle = Ariticles.query.get_or_404(ariticles_id)
    db.session.delete(ariticle)
    db.session.commit()
    flash('删除数据成功')
    return redirect(url_for('index'))

# 用户登录 flask提供的login_user()函数
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('输入错误')
            return redirect(url_for('login'))
        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登录用户
            flash('登录成功')
            return redirect(url_for('index'))  # 登录成功返回首页
        flash('用户名或密码输入错误')
        return redirect(url_for('login'))
    return render_template('login.html')

# 用户登出
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出登录')
    return redirect(url_for('index'))
@app.route('/add',methods=['GET','POST'])
def add():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        # 获取表单的数据
        title = request.form.get('title')
        author = request.form.get('author')
        pubdate = request.form.get('pubdate')
        content = request.form.get('content')

        # 验证不为空
        if not title or not author or not pubdate or not content or len(author)>6 or len(title)>60:
            flash('输入错误')  # 错误提示
            return redirect(url_for('index'))  # 重定向回主页
        
        ariticle = Ariticles(title=title,author=author,pubdate=pubdate,content=content)  # 创建记录
        db.session.add(ariticle)  # 添加到数据库会话
        db.session.commit()   # 提交数据库会话
        flash('数据创建成功')
        return redirect(url_for('index'))
    return render_template('add.html')
