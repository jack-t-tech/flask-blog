from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models import User, Post
from flask_login import login_required, current_user, login_user, logout_user
from extensions import db
from forms.user_forms import LoginForm, Profile
from . import blog_bp


@blog_bp.route('/admin')
@login_required
def admin():
    return render_template('/admin/admin.html')

@blog_bp.route('/blog_list', methods=['GET'])
def blog_list():
    posts = Post.query.all()
    return render_template('/admin/blog_list.html', posts=posts)

@blog_bp.route('/blog_listuser', methods=['GET'])
def blog_listuser():
    posts = Post.query.all()
    return render_template('/user/blog_list.html', posts=posts)
    
@blog_bp.route('/post_admin_detail/<int:post_id>', methods=['GET'])
@login_required
def post_admin_detail(post_id):
    post = Post.query.get(post_id)
    return render_template('/admin/blog_admin_detail.html', post=post)

@blog_bp.route('/post_user_detail/<int:post_id>', methods=['GET'])
def post_user_detail(post_id):
    post = Post.query.get(post_id)
    return render_template('/user/blog_user_detail.html', post=post)

@blog_bp.route('/edit_post/<int:post_id>', methods=['POST', 'GET'])
@login_required
def edit_post(post_id):
    post = Post.query.get(post_id)
    if request.method == 'GET':
        return render_template('/admin/edit_post.html', post=post)
    elif request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('blog.blog_list'))

@blog_bp.route('/delete_post/<int:post_id>', methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.blog_list'))

@blog_bp.route('/add_post', methods=['POST', 'GET'])
@login_required
def add_post():
    if request.method == 'GET':
        return render_template('/admin/add_post.html')
    elif request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = current_user.id 
        post = Post(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog.blog_list'))

@blog_bp.route('/profile')
@login_required
def profile():
    user = current_user
    return render_template('/user/profile.html', user=user)

@blog_bp.route('/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    user = current_user
    if request.method == 'GET':
        return render_template('edit_profile.html', user=user)
    elif request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        db.session.commit()
        return redirect(url_for('blog.profile'))
    
