from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models import Role, User
from extensions import db
from forms.user_forms import LoginForm, Profile
from flask_login import login_user, login_required, logout_user, current_user

user_bp = Blueprint('user', __name__, template_folder='templates')


@user_bp.route('/add_user', methods=['POST', 'GET'])
def add_user():
    if request.method == 'GET':
        return render_template('user/add_user.html')
    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = User(username=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.login'))

@user_bp.route('/signup', methods=['POST', 'GET'])
def signup():
    form = Profile()
    if request.method == 'GET':
        return render_template('user/signup.html', form=form)
    elif request.method == 'POST' and form.validate_on_submit():
        name = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(username=name, email=email)
        user.password = password # ハッシュ化　modelsで定義したpassword.setterを呼び出す
        db.session.add(user)
        db.session.commit()
        flash('You were successfully registered', 'alert-success')
        return redirect(url_for('user.login'))
    flash('Invalid input', 'alert-danger')
    return render_template('user/signup.html', form=form)

@user_bp.route('/profile', methods=['GET'])
def profile():
    user = current_user
    return render_template('user/profile.html', user=user)

@user_bp.route('/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    form = Profile()
    
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.role.data = current_user.role
        return render_template('user/edit_profile.html', form=form)
    elif request.method == 'POST' and form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.password.data:
            current_user.password = form.password.data
        flash('Profile updated', 'alert-success')
        db.session.commit()
        return redirect(url_for('user.edit_profile'))
    return render_template('user/edit_profile.html', form=form)

@user_bp.route('/user_list', methods=['POST', 'GET'])
@login_required
def user_list():
    users = User.query.all()
    if current_user.role.name != 'admin':
        flash('You are not authorized', 'alert-danger')
        return redirect(url_for('blog.admin'))

    if request.method == 'POST':
        user_id = request.form.get('user_id')  # フォームからユーザーIDを取得
        new_role = request.form.get('role')   # フォームから新しいロールを取得
        print(new_role)
        role = Role.query.filter_by(name=new_role).first()  # ロール名からRoleオブジェクトを取得
        user = User.query.get(user_id)

        if not user:
            flash('User not found', 'alert-danger')
            return redirect(url_for('user.user_list'))

        # ユーザーのロールを更新
        user.role_id = role.id 
        db.session.commit()
        flash('Role updated', 'alert-success')
        return redirect(url_for('user.user_list'))

    return render_template('admin/user_list.html', users=users)


@user_bp.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    user_id = request.form['user_id']
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted', 'alert-success')
    return redirect(url_for('user.user_list'))

@user_bp.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('user/login.html', form=form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            flash('You were successfully logged in', 'alert-success')
            return redirect(url_for('blog.admin'))
        else:
            flash('Invalid email or password', 'alert-danger')

    return render_template('user/login.html', form=form)


@user_bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('You were successfully logged out', 'alert-success')
    return redirect(url_for('user.login'))

