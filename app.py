from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from pytz import timezone
from sqlalchemy.sql import func
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, server_default=func.now(), nullable=True)



@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    if request.method == 'GET':
        return render_template('add_user.html')
    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = User(username=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('user/signup.html')
    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = User(username=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:    
            session['user_id'] = user.id
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('login'))

@app.route('/logout')  
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))



@app.route('/admin')
def admin():
    return render_template('/admin/admin.html')
#admin-bloglist
@app.route('/blog_list', methods=['GET'])
def blog_list():
    posts = Post.query.all()
    return render_template('/admin/blog_list.html', posts=posts)

@app.route('/edit_post/<int:id>', methods=['POST', 'GET'])
def edit_post(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('edit_post.html', post=post)
    elif request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('posts'))

@app.route('/add_post', methods=['POST', 'GET'])
def add_post():
    if request.method == 'GET':
        return render_template('/admin/add_post.html')
    elif request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = session['user_id']
        post = Post(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog_list'))

@app.route('/profile')
def profile():
    user_id = session['user_id']
    user = User.query.get(user_id)
    return render_template('/user/profile.html', user=user)

@app.route('/edit_profile', methods=['POST', 'GET'])
def edit_profile():
    user_id = session['user_id']
    user = User.query.get(user_id)
    if request.method == 'GET':
        return render_template('edit_profile.html', user=user)
    elif request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        db.session.commit()
        return redirect(url_for('profile'))

# Error Handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('/errors/404.html', error=e), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('/errors/500.html', error=e), 500



if __name__ == '__main__':
    app.run(debug=True)
    
