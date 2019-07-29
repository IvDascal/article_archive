from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, UserCreateForm, UserEditForm
from app.models import User, Role


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.verify_password(form.password.data):
            # TODO error message
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<int:id>')
def user(id):
    user = User.query.get(id)

    return render_template('user_detail.html', user=user)


@app.route('/users')
def users():
    users = User.query.all()
    print(users)
    return render_template('users.html', users=users)


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    form = UserCreateForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        user.is_active = form.is_active.data
        print(form.role.data)
        role = Role.query.get(form.role.data)
        user.role = role
        print(user)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('users'))

    return render_template('create_user.html', form=form)


@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get(id)
    form = UserEditForm(user=user)
    print(user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.is_active = form.is_active.data
        role = Role.query.get(form.role.data)
        user.role = role

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('user', id=user.id))

    form.email.data = user.email
    form.username.data = user.username
    form.role.data = user.role_id

    return render_template('edit_user.html', form=form)


@app.route('/delete_user/<int:id>')
def delete_user(id):
    user = User.query.get(id)
    user.is_active = False

    db.session.add(user)
    db.session.commit()

    # TODO delete confirmation to avoid misclick
    # TODO success  or error message

    return redirect(url_for('users'))
