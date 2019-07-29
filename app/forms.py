from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError

from app.models import Role, User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class UserCreateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    is_active = BooleanField('Active', default="checked")
    role = SelectField('Role', coerce=int)
    submit = SubmitField('Create')

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class UserEditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    is_active = BooleanField('Active', default="checked")
    role = SelectField('Role', coerce=int)
    submit = SubmitField('Save')

    def __init__(self, user, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)

        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first(): raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first(): raise ValidationError('Username already in use.')


class SourceCreateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    sid = StringField('SID', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    is_active = BooleanField('Active', default="checked")
    submit = SubmitField('Create')


class SourceEditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    sid = StringField('SID', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    is_active = BooleanField('Active', default="checked")
    submit = SubmitField('Edit')

    def __init__(self, source, *args, **kwargs):
        super(SourceEditForm, self).__init__(*args, **kwargs)

        self.source = source
