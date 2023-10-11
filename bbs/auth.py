from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, url_for, redirect, flash, escape, abort
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user
from bbs import db, app
from icecream import ic

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(id):
    userjson = db.get_user_by_id(id)
    user = User(userjson)
    return user

login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, *initial_data, **kwargs):
        super().__init__()
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get_id(self):
        return self.id

    def set_password(self, password) -> None:
        self.password_hash = generate_password_hash(password)
        # self.password_hash = password
    
    def validate_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)
        # return password == self.password_hash

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html.jinja')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        userid = db.get_userid_by_name(username)
        if userid != None:
            userjson = db.get_user_by_id(userid)
            userjson['password_hash'] = userjson['password']
            user = User(userjson)
            if user.validate_password(password):
                login_user(user)
                # flash('登陆成功')
                return redirect(url_for('index'))

        flash('用户名或密码错误')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html.jinja')

    if request.method == 'POST':
        if request.form.get('agree') == None:
            flash('请阅读用户协议')
            return redirect(url_for('register'))

        username = request.form['username']
        password = request.form['password']
        password_conf = request.form['confirm-password']

        if password != password_conf:
            flash('确认密码不一致')
            return redirect(url_for('register'))

        new_user = User(username=username)
        new_user.set_password(password)

        if db.add_user(new_user.username, new_user.password_hash) == True:
            flash('注册成功')
            return redirect(url_for('login'))
        else:
            flash('用户名已存在')
            return redirect(url_for('register'))