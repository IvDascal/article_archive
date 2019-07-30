from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, UserCreateForm, UserEditForm, SourceCreateForm, SourceEditForm, DocumentEditForm, \
    DocumentCreateForm
from app.models import User, Role, Source, Document


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

        role = Role.query.get(form.role.data)
        user.role = role

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('users'))

    return render_template('create_user.html', form=form)


@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get(id)
    form = UserEditForm(user=user)

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


@app.route('/source/<int:id>')
def source(id):
    source = Source.query.get(id)

    return render_template('source_detail.html', source=source)


@app.route('/sources')
def sources():
    sources = Source.query.all()

    return render_template('sources.html', sources=sources)


@app.route('/source_create', methods=['GET', 'POST'])
def source_create():
    form = SourceCreateForm()
    if form.validate_on_submit():
        source = Source()
        source.sid = form.sid.data
        source.name = form.name.data
        source.url = form.url.data

        db.session.add(source)
        db.session.commit()

        return redirect(url_for('sources'))

    return render_template('source_create.html', form=form)


@app.route('/source_edit/<int:id>', methods=['GET', 'POST'])
def source_edit(id):
    source = Source.query.get(id)
    form = SourceEditForm(source=source)

    if form.validate_on_submit():
        source.sid = form.sid.data
        source.name = form.name.data
        source.url = form.url.data

        db.session.add(source)
        db.session.commit()

        return redirect(url_for('source', id=source.id))

    form.sid.data = source.sid
    form.name.data = source.name
    form.url.data = source.url

    return render_template('source_edit.html', form=form)


@app.route('/source_delete/<int:id>')
def source_delete(id):
    source = Source.query.get(id)
    source.is_active = False

    db.session.add(source)
    db.session.commit()

    # TODO delete confirmation to avoid misclick
    # TODO success  or error message

    return redirect(url_for('sources'))


@app.route('/document/<int:id>')
def document(id):
    document = Document.query.get(id)

    return render_template('document_detail.html', document=document)


@app.route('/documents')
def documents():
    documents = Document.query.all()

    return render_template('documents.html', documents=documents)


@app.route('/document_create', methods=['GET', 'POST'])
def document_create():
    form = DocumentCreateForm()
    if form.validate_on_submit():
        document = Document()
        document.title = form.title.data
        document.text = form.text.data
        document.url = form.url.data
        document.created = form.created.data
        source = Source.query.get(form.source.data)
        document.source = source
        user = User.query.get(form.user.data)
        document.user = user

        db.session.add(document)
        db.session.commit()

        return redirect(url_for('documents'))

    return render_template('document_create.html', form=form)


@app.route('/document_edit/<int:id>', methods=['GET', 'POST'])
def document_edit(id):
    document = Document.query.get(id)
    form = DocumentEditForm(document=document)

    if form.validate_on_submit():
        document.title = form.title.data
        document.text = form.text.data
        document.url = form.url.data
        document.created = form.created.data
        source = Source.query.get(form.source.data)
        document.source = source
        user = User.query.get(form.user.data)
        document.user = user

        db.session.add(document)
        db.session.commit()

        return redirect(url_for('document', id=document.id))

    form.title.data = document.title
    form.text.data = document.text
    form.url.data = document.url
    form.created.data = document.created
    form.source.data = document.source
    form.user.data = document.user

    return render_template('document_edit.html', form=form)


@app.route('/document_delete/<int:id>')
def document_delete(id):
    document = Document.query.get(id)

    db.session.delete(document)
    db.session.commit()

    # TODO delete confirmation to avoid misclick
    # TODO success or error message

    return redirect(url_for('documents'))
